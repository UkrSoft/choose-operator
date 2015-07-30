import datetime
from django.views.generic import TemplateView

class MainView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(MainView, self).get_context_data(**kwargs)
        context['now'] = datetime.datetime.now()
        # Sequence of operations (app logic):
        # 1) get input:
        #   get source operator preferences: mts, kyivstar, life; - percentage; sum of the criteria values should be 100%
        #   get target operator preferences: mts, kyivstar, life; - percentage; sum of the criteria values should be 100%
        #   get target usage preferences: data, sms, calls, international calls? - percentage; sum of the criteria values should be 100%
        #   get money preferences: what is monthly limit for you (slider) - integer, "0" by default, this means "no limit"
        #
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
        #
        # 3) output data:
        #   output packages on the results page
        #   use the same template as for data input (only difference is - pass resulting table parameter to template)
        #   packages to be grouped inside of the template (it is cheep operation, because little amount of packages to be shown on the page)
        #   table headers will be transposed to row names (this will be the feature names) in the resulting page
        #   each table row will be transposed to separate column with 1 package in it
        return context