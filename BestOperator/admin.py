from django.contrib import admin

from BestOperator.forms import FeatureForm, PaymentForm, \
    SmallLinkForm
from BestOperator.funcs import get_editable_fields, expand_list_both_sides
from .models import *

__author__ = 'Kostiantyn Bezverkhyi'

#Start common inline model
class CIM(admin.StackedInline):
    extra = 0
    show_change_link = True
#End common inline model

#Start inlines
class LocationLocationAdmin(CIM):
    model = Location
    fieldsets = [(None, {'fields' : ['name', 'location_type']})]

class OfferFeatureInline(CIM):
    model = Feature
    fieldsets = [(None, {'fields': ['service']}), ]

class PackageOfferInline(CIM):
    model = Offer.package.through
    readonly_fields = ['terms', 'url']
    def url(self, instance):
        return instance.offer.get_absolute_url_link()
    def terms(self, instance):
        return instance.offer.po_term

class OperatorPackageInline(CIM):
    form = SmallLinkForm
    model = Package
    fieldsets = [(None, {'fields': ['name', 'package_type', 'price', 'link']}), ]
#End inlines

#Start common admin model
class CAM(admin.ModelAdmin):
    list_disp_start = ['gab', ]
    list_disp_end = ['remove', ]
    list_display_links = ['gab', ]
    view_on_site = False
    save_on_top = True
    save_as = True
    # search_fields = ['name', ] #TODO add search fields
    #TODO add sorting to models in the admin
    def get_actions(self, request):
        actions = super(CAM, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
#End common admin model

def expand_list_display(my_list):
    return expand_list_both_sides(my_list, CAM.list_disp_start, CAM.list_disp_end)

#Start admin models
class PackageTypeAdmin(CAM):
    list_display = expand_list_display(['name', 'description'])
    list_editable = get_editable_fields(PackageType, list_display)
    fieldsets = [
        (None,                {'fields': [('name', ), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class PackageAdmin(CAM):
    form = SmallLinkForm
    list_filter = ['operator', 'package_type', 'po_term__is_active']
    list_display = expand_list_display(['name', 'operator', 'package_type', 'po_term', 'price'])
    list_editable = get_editable_fields(Package, list_display)
    fieldsets = [
        (None,                {'fields': [('name', 'link')]}),
        ('Operator Info',     {'fields': [('operator', 'package_type', ), ]}),
        ('Payment Info',      {'fields': [('po_term', 'price', ), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]
    inlines = [PackageOfferInline, ]

class OfferAdmin(CAM):
    form = SmallLinkForm
    filter_horizontal = ['package', ]
    list_filter = ['po_term__is_active', 'package']
    list_display = expand_list_display(['name', 'packages', 'po_term'])
    list_editable = get_editable_fields(Offer, list_display)
    fieldsets = [
        (None,                  {'fields': [('name', 'link', ), ]}),
        ('Linked to',           {'fields': [('package', 'po_term'), ]}),
        ('Extra',               {'fields': ['description'], 'classes':['collapse']}),
    ]
    inlines = [OfferFeatureInline, ]

class FeatureAdmin(CAM):
    form = FeatureForm
    list_filter = ['service', ]
    readonly_fields = ['name', ]
    list_display = expand_list_display(['name', 'service', 'package', 'offer'])
    list_editable = get_editable_fields(Feature, list_display)
    fieldsets = [
        (None,                {'fields': ['name', 'service', ]}),
        ('Linked to',         {'fields': [('package', 'offer'), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class PaymentAdmin(CAM):
    form = PaymentForm
    list_filter = ['period', 'term_of_usage__service_type', 'term_of_usage']
    readonly_fields = ['name', ]
    list_display = expand_list_display(['name', 'feature', 'offer', 'period', 'term_of_usage'])
    list_editable = get_editable_fields(Payment, list_display)
    fieldsets = [
        (None,                {'fields': [('name', 'feature', 'offer'), ]}),
        ('Pricing options',   {'fields': [('period', 'price', 'term_of_usage'), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]
    def name(self, instance):
        return instance.__str__()
    name.short_description = 'Name'

class PeriodAdmin(CAM):
    list_filter = ['num_of_days', ]
    list_display = expand_list_display(['name', 'num_of_days', 'from_time', 'to_time'])
    list_editable = get_editable_fields(Period, list_display)
    fieldsets = [
        (None,                {'fields': [('name', 'num_of_days'), ]}),
        ('Periods',           {'fields': [('from_time', 'to_time'),]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class POTermAdmin(CAM):
    readonly_fields = ['name', ]
    list_filter = ['is_active', ]
    list_display = expand_list_display(['name', 'is_active', 'active_from_date', 'active_to_date', 'order_from_date', 'order_to_date'])
    list_editable = get_editable_fields(POTerm, list_display)
    fieldsets = [
        (None,                {'fields': ['name', 'is_active', ]}),
        ('Active',            {'fields': [('active_from_date', 'active_to_date'), ]}),
        ('Can buy',           {'fields': [('order_from_date', 'order_to_date'), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class ServiceTypeAdmin(CAM):
    list_filter = ['is_displayed', ]
    list_display = expand_list_display(['name', 'description'])
    list_editable = get_editable_fields(ServiceType, list_display)
    fieldsets = [
        (None,                {'fields': [('name', 'is_displayed'), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class LocationTypeAdmin(CAM):
    list_display = expand_list_display(['name', 'description'])
    list_editable = get_editable_fields(LocationType, list_display)
    fieldsets = [
        (None,                {'fields': [('name', ), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class LocationAdmin(CAM):
    list_filter = ['location_type', 'included_in']
    list_display = expand_list_display(['name', 'location_type', 'included_in'])
    list_editable = get_editable_fields(Location, list_display)
    fieldsets = [
        (None,                {'fields': [('name', 'location_type'), ]}),
        ('Pricing options',   {'fields': [('included_in', ), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]
    inlines = [LocationLocationAdmin, ]

class ServicesAdmin(CAM):
    list_filter = ['service_type', 'direction__to_location', 'direction__to_operator']
    list_display = expand_list_display(['name', 'service_type', 'direction'])
    list_editable = get_editable_fields(Service, list_display)
    fieldsets = [
        (None,                {'fields': ['name', ]}),
        ('Reference Info',    {'fields': [('service_type', 'direction'), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class OperatorAdmin(CAM):
    form = SmallLinkForm
    list_filter = ['location', ]
    list_display = expand_list_display(['name', 'location', 'description'])
    list_editable = get_editable_fields(Operator, list_display)
    fieldsets = [
        (None,                {'fields': [('name', 'link')]}),
        ('Location Info',     {'fields': [('location', ), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]
    inlines = [OperatorPackageInline, ]

class ParamAdmin(CAM):
    list_filter = ['attr', ]
    readonly_fields = ['name', ]
    list_display = expand_list_display(['name', 'attr', 'value', 'feature'])
    list_editable = get_editable_fields(Param, list_display)
    fieldsets = [
        (None,                {'fields': ['name', ('attr', 'value'), ]}),
        ('Linked to',         {'fields': [('feature', ), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class TermsOfUsageAdmin(CAM):
    list_filter = ['amount', 'service_type']
    readonly_fields = ['name', ]
    list_display = expand_list_display(['name', 'criterion', 'amount', 'unit'])
    list_editable = get_editable_fields(TermOfUsage, list_display)
    fieldsets = [
        (None,                {'fields': ['name', ('criterion', 'amount', 'unit'), ]}),
        ('Linked to',         {'fields': ['service_type', ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class AttributeAdmin(CAM):
    list_filter = ['service_type', 'unit']
    list_display = expand_list_display(['name', 'service_type', 'unit'])
    list_editable = get_editable_fields(Attribute, list_display)
    fieldsets = [
        (None,                {'fields': [('service_type', 'name', 'unit'), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class UnitAdmin(CAM):
    list_display = expand_list_display(['unit', 'compared_to', 'multiplier'])
    list_editable = get_editable_fields(Unit, list_display)
    fieldsets = [
        (None,                {'fields': [('name', 'unit'), ]}),
        ('Self reference',    {'fields': [('compared_to', 'multiplier'), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class CriterionAdmin(CAM):
    list_display = expand_list_display(['name', 'description'])
    list_editable = get_editable_fields(Criterion, list_display)
    fieldsets = [
        (None,                {'fields': [('name', ), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class DirectionAdmin(CAM):
    list_filter = ['from_location', 'to_location', 'to_operator']
    readonly_fields = ['name', ]
    list_display = expand_list_display(['name', 'from_location', 'to_location', 'to_operator'])
    list_editable = get_editable_fields(Direction, list_display)
    fieldsets = [
        (None,                {'fields': ['name', ('from_location', 'to_location', ), ]}),
        ('Linked to',         {'fields': [('to_operator', ), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class CodeAdmin(CAM):
    list_filter = ('operator', )
    list_display = expand_list_display(['operator_code', 'operator'])
    list_editable = get_editable_fields(Code, list_display)
    fieldsets = [
        (None,                {'fields': [('operator', 'operator_code', ), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class DirectoryAdmin(CAM):
    list_filter = ('changed_date', )
    list_display = expand_list_display(['key', 'value', 'changed_date'])
    list_editable = get_editable_fields(Directory, list_display)
    fieldsets = [
        (None,                {'fields': [('key', 'value', ), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

admin.site.register(Direction, DirectionAdmin)
admin.site.register(ServiceType, ServiceTypeAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Service, ServicesAdmin)
admin.site.register(Operator, OperatorAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Param, ParamAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Period, PeriodAdmin)
admin.site.register(POTerm, POTermAdmin)
admin.site.register(Criterion, CriterionAdmin)
admin.site.register(TermOfUsage, TermsOfUsageAdmin)
admin.site.register(LocationType, LocationTypeAdmin)
admin.site.register(PackageType, PackageTypeAdmin)
admin.site.register(Directory, DirectoryAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Code, CodeAdmin)

