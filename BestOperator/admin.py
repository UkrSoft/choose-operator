from django.contrib import admin

from BestOperator.forms import FeatureForm, PaymentForm, \
    SmallLinkForm
from BestOperator.funcs import get_editable_fields, expand_list_unique, \
    get_existent_fields
from .models import *

__author__ = 'Kostiantyn Bezverkhyi'

#Start common inline model
class CIM(admin.StackedInline):
    extra = 0
    show_change_link = True
    view_on_site = False
#End common inline model
#todo improve general perception and linkage of the admin pages
#TODO make [Save] button on top of the model list page
#Start inlines
class LocationLocationAdmin(CIM):
    model = Location
    fieldsets = [(None, {'fields' : ['name', 'location_type']})]

class OfferFeatureInline(CIM):
    model = Feature
    fieldsets = [(None, {'fields': ['service', 'service__service_type', 'service__direction', ]}), ]
    readonly_fields = ['service__service_type', 'service__direction', ]
    def service__service_type(self, instance):
        return instance.service.service_type
    service__service_type.short_description = 'Service Type'
    def service__direction(self, instance):
        return instance.service.direction
    service__direction.short_description = 'Service Direction'

class PackageOfferInline(CIM):
    model = Offer.package.through
    fieldsets = [(None, {'fields': [('offer', 'url'), 'terms', ('terms__active_from_date', 'terms__active_to_date')
                                    , ('terms__order_from_date', 'terms__order_to_date')
                                    ]}), ]
    readonly_fields = ['terms', 'url', 'terms__active_from_date', 'terms__active_to_date'
                                    , 'terms__order_from_date', 'terms__order_to_date']
    verbose_name = 'Offer'
    verbose_name_plural = 'Offers'
    def url(self, instance):
        return instance.offer.get_absolute_url_link()
    url.allow_tags = True
    def terms(self, instance):
        return instance.offer.po_term
    def terms__active_from_date(self, instance):
        return instance.offer.po_term.active_from_date
    terms__active_from_date.short_description = 'Active From'
    def terms__active_to_date(self, instance):
        return instance.offer.po_term.active_to_date
    terms__active_to_date.short_description = 'Active To'
    def terms__order_from_date(self, instance):
        return instance.offer.po_term.order_from_date
    terms__order_from_date.short_description = 'Order From'
    def terms__order_to_date(self, instance):
        return instance.offer.po_term.order_to_date
    terms__order_to_date.short_description = 'Order To'

class OperatorPackageInline(CIM):
    form = SmallLinkForm
    model = Package
    fieldsets = [(None, {'fields': [('name', 'package_type', 'link'), ('po_term', 'price')]}), ]
#End inlines

#Start common admin model
class CAM(admin.ModelAdmin):
    view_on_site = False
    save_on_top = True
    save_as = True
    list_per_page = 20
    def gim(in_model, in_list_display):
        list_display = expand_list_unique(['get_pk', ], in_list_display, ['remove', ])#'name',
        list_editable = [f.name for f in get_editable_fields(in_model, list_display)]
        search_fields = [f.name for f in get_existent_fields(in_model, ['name', ])]
        list_display_links = ['get_pk', ] #if get_editable_fields(in_model, ['name', ]).__len__()>0 else ['name', ]
        return list_display, list_editable, search_fields, list_display_links
    def get_actions(self, request):
        actions = super(CAM, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions
#End common admin model

#Start admin models
class PackageTypeAdmin(CAM):
    list_display, list_editable, search_fields, list_display_links = CAM.gim(PackageType, ['name', 'description'])
    fieldsets = [
        (None,                {'fields': [('name', ), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class PackageAdmin(CAM):
    form = SmallLinkForm
    list_filter = ['operator', 'package_type', 'po_term__is_active']#TODO re-write admin.register to include this logic
    list_display, list_editable, search_fields, list_display_links = CAM.gim(Package, ['name', 'operator', 'package_type', 'po_term', 'price'])
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
    list_display, list_editable, search_fields, list_display_links = CAM.gim(Offer, ['name', 'packages', 'po_term'])
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
    list_display, list_editable, search_fields, list_display_links = CAM.gim(Feature, ['name', 'service', 'package', 'offer'])
    fieldsets = [
        (None,                {'fields': ['name', 'service', ]}),
        ('Linked to',         {'fields': [('package', 'offer'), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class PaymentAdmin(CAM):
    form = PaymentForm
    list_filter = ['period', 'term_of_usage__service_type', 'term_of_usage']
    # readonly_fields = ['name', ]
    list_display, list_editable, search_fields, list_display_links = CAM.gim(Payment, ['feature', 'offer', 'period', 'term_of_usage'])#'name',
    fieldsets = [
        (None,                {'fields': [('name', 'feature', 'offer'), ]}),
        ('Pricing options',   {'fields': [('period', 'price', 'term_of_usage'), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class PeriodAdmin(CAM):
    list_filter = ['num_of_days', ]
    list_display, list_editable, search_fields, list_display_links = CAM.gim(Period, ['name', 'num_of_days', 'from_time', 'to_time'])
    fieldsets = [
        (None,                {'fields': [('name', 'num_of_days'), ]}),
        ('Periods',           {'fields': [('from_time', 'to_time'),]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class POTermAdmin(CAM):
    # readonly_fields = ['name', ]
    list_filter = ['is_active', ]
    list_display, list_editable, search_fields, list_display_links = CAM.gim(POTerm, ['is_active', 'active_from_date', 'active_to_date', 'order_from_date', 'order_to_date'])#'name',
    fieldsets = [
        (None,                {'fields': ['name', 'is_active', ]}),
        ('Active',            {'fields': [('active_from_date', 'active_to_date'), ]}),
        ('Can buy',           {'fields': [('order_from_date', 'order_to_date'), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class ServiceTypeAdmin(CAM):
    list_filter = ['is_displayed', ]
    list_display, list_editable, search_fields, list_display_links = CAM.gim(ServiceType, ['name', 'description'])
    fieldsets = [
        (None,                {'fields': [('name', 'is_displayed'), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class LocationTypeAdmin(CAM):
    list_display, list_editable, search_fields, list_display_links = CAM.gim(LocationType, ['name', 'description'])
    fieldsets = [
        (None,                {'fields': [('name', ), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class LocationAdmin(CAM):
    list_filter = ['location_type', 'included_in']
    list_display, list_editable, search_fields, list_display_links = CAM.gim(Location, ['name', 'location_type', 'included_in'])
    fieldsets = [
        (None,                {'fields': [('name', 'location_type'), ]}),
        ('Pricing options',   {'fields': [('included_in', ), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]
    inlines = [LocationLocationAdmin, ]

class ServicesAdmin(CAM):
    list_filter = ['service_type', 'direction__to_location', 'direction__to_operator']
    # readonly_fields = ['name', ]
    list_display, list_editable, search_fields, list_display_links = CAM.gim(Service, ['service_type', 'direction'])#'name',
    fieldsets = [
        (None,                {'fields': ['name', ]}),
        ('Reference Info',    {'fields': [('service_type', 'direction'), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class OperatorAdmin(CAM):
    form = SmallLinkForm
    list_filter = ['location', ]
    list_display, list_editable, search_fields, list_display_links = CAM.gim(Operator, ['name', 'location'])
    fieldsets = [
        (None,                {'fields': [('name', 'location', 'link')]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]
    inlines = [OperatorPackageInline, ]

class ParamAdmin(CAM):
    list_filter = ['attr', ]
    # readonly_fields = ['name', ]
    list_display, list_editable, search_fields, list_display_links = CAM.gim(Param, ['attr', 'value', 'feature'])#'name',
    fieldsets = [
        (None,                {'fields': ['name', ('attr', 'value'), ]}),
        ('Linked to',         {'fields': [('feature', ), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class TermsOfUsageAdmin(CAM):
    list_filter = ['amount', 'service_type']
    readonly_fields = ['name', ]
    list_display, list_editable, search_fields, list_display_links = CAM.gim(TermOfUsage, ['name', 'criterion', 'amount', 'unit'])
    fieldsets = [
        (None,                {'fields': ['name', ('criterion', 'amount', 'unit'), ]}),
        ('Linked to',         {'fields': ['service_type', ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class AttributeAdmin(CAM):
    list_filter = ['service_type', 'unit']
    list_display, list_editable, search_fields, list_display_links = CAM.gim(Attribute, ['name', 'service_type', 'unit'])
    fieldsets = [
        (None,                {'fields': [('service_type', 'name', 'unit'), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class UnitAdmin(CAM):
    list_display, list_editable, search_fields, list_display_links = CAM.gim(Unit, ['unit', 'compared_to', 'multiplier'])
    fieldsets = [
        (None,                {'fields': [('name', 'unit'), ]}),
        ('Self reference',    {'fields': [('compared_to', 'multiplier'), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class CriterionAdmin(CAM):
    list_display, list_editable, search_fields, list_display_links = CAM.gim(Criterion, ['name', 'description'])
    fieldsets = [
        (None,                {'fields': [('name', ), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class DirectionAdmin(CAM):
    list_filter = ['from_location', 'to_location', 'to_operator']
    readonly_fields = ['name', ]
    list_display, list_editable, search_fields, list_display_links = CAM.gim(Direction, ['name', 'from_location', 'to_location', 'to_operator'])
    fieldsets = [
        (None,                {'fields': ['name', ('from_location', 'to_location', ), ]}),
        ('Linked to',         {'fields': [('to_operator', ), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class CodeAdmin(CAM):
    list_filter = ('operator', )
    list_display, list_editable, search_fields, list_display_links = CAM.gim(Code, ['operator_code', 'operator'])
    fieldsets = [
        (None,                {'fields': [('operator', 'operator_code', ), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]

class DirectoryAdmin(CAM):
    list_filter = ('changed_date', )
    list_display, list_editable, search_fields, list_display_links = CAM.gim(Directory, ['key', 'value', 'changed_date'])
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

