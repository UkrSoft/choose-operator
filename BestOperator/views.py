from django.template import RequestContext
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from BestOperator.funcs import MagicSql
from BestOperator.models import Operator, ServiceType

class MainView(TemplateView):
    template_name = "BestOperator/index.html"

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['operators'] = Operator.objects.all()
        context['serviceTypes'] = ServiceType.objects.filter(is_displayed=True)
        return context

def post_results(request):
    if (request.method!='POST'):
        return HttpResponseRedirect(reverse('boo:index'))
    try:#TODO make not all parameters required. Basically we could run this without any params at all
        # 1) get input:
        #   get source operator preferences: mts, kyivstar, life; - percentage; sum of the criteria values should be 100%
        #   get target operator preferences: mts, kyivstar, life; - percentage; sum of the criteria values should be 100%
        #   get target usage preferences: data, sms, calls, international calls? - percentage; sum of the criteria values should be 100%
        #   get money preferences: what is monthly limit for you (slider) - integer, "0" by default, this means "no limit"
        fromOperators = Operator.objects.filter(pk=request.POST['from_operators'])
        toOperators = Operator.objects.filter(pk=request.POST['to_operators'])
        preferredServices = ServiceType.objects.filter(pk=request.POST['pref_services'])
        moneyLimit = request.POST['money_limit']
    except (KeyError, Operator.DoesNotExist, ServiceType.DoesNotExist):
        # Redisplay the question voting form.
        context = RequestContext(request, {
            'error_message': "Ви не зробили свій вибір.",
        })
        return render(request, 'BestOperator/index.html', context)#TODO HttpResponseRedirect
    else:
        sql = 'select  ' \
        '    o.name as oper_name' \
        '    , p.id as pack_id' \
        '    , p.name as pack_name' \
        '    , p.description as pack_descr' \
        '    , p.price as pack_price' \
        '    , p.link as pack_link' \
        '    , off.id as offer_id' \
        '    , off.name as offer_name' \
        '    , f.id as feature_id' \
        '    , s.id as service_id' \
        '    , s.name as service_name' \
        '    , st.id as st_id' \
        '    , st.name as st_name' \
        '    , a.name as attr' \
        '    , par.value as val ' \
        'from  ' \
        '    bestoperator_operator o' \
        '    join bestoperator_package p on p.operator_id = o.id' \
        '    left join bestoperator_feature f on f.package_id = p.id' \
        '    left join bestoperator_offer off on f.offer_id = off.id' \
        '    left join bestoperator_offer_package_id oftp on oftp.package_id = p.id and oftp.offer_id = off.id' \
        '    left join bestoperator_service s on f.service_id = s.id' \
        '    left join bestoperator_servicetype st on st.id = s.service_type_id' \
        '    left join bestoperator_param par on par.feature_id = f.id' \
        '    left join bestoperator_attribute a on par.attr_id = a.id'
        sqlRows = MagicSql(sql).get_named_tuple()
        # 2) make calculations:
        #   this would be just one multi-table join SQL query
        #       input parameters filtering list will be concatenated as dynamic SQL at runtime just BEFORE script execution.
        #       get value of how valuable each criteria is (%)
        #   select list of packages which are most valuable:
        #       each package has features. Each feature should have "how good" value assigned
        #       this assigned value will be multiplied on target %
        #       all package criteria resulting values should be summarized
        #   packages should be sorted by this resulting sum
        #   results should be represented as list of rows - 1 row for the separate package to output
        context = RequestContext(request, {
            'sqlRows': sqlRows,
        })
        # 3) output data:
        #   output packages on the results page
        #   use the same template as for data input (only difference is - pass resulting table parameter to template)
        #   packages to be grouped inside of the template (it is cheep operation, because little amount of packages to be shown on the page)
        #   table headers will be transposed to row names (this will be the feature names) in the resulting page
        #   each table row will be transposed to separate column with 1 package in it
        return render(request, 'BestOperator/results.html', context)#TODO HttpResponseRedirect