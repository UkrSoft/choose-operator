from django.contrib import admin

from BestOperator.forms import FeatureForm, PaymentForm, OfferForm, \
    SmallLinkForm
from .models import *

__author__ = 'Kostiantyn Bezverkhyi'

class FeatureInline(admin.TabularInline):
    model = Feature
    fk_name = 'offer'
    fieldsets = [(None, {'fields': ['service']}), ]
    extra = 0

class PackageOfferInline(admin.TabularInline):
    model = Offer.package.through
    readonly_fields = ['terms', 'url']
    def url(self, instance):
        return instance.offer.get_absolute_url_link()
    def terms(self, instance):
        return instance.offer.po_term
    extra = 0

class OperatorPackageInline(admin.TabularInline):
    form = SmallLinkForm
    show_change_link = True
    model = Package
    fieldsets = [(None, {'fields': ['name', 'package_type', 'price', 'link']}), ]
    extra = 0

class OfferAdmin(admin.ModelAdmin):
    form = OfferForm
    filter_horizontal = ('package', )
    list_display = ('name', 'packages', 'po_term')
    fieldsets = [
        (None,                {'fields': [('name', 'link', ), ]}),
        ('Linked to',           {'fields': [('package', 'po_term'), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]
    inlines = [FeatureInline, ]
    save_on_top = True

class FeatureAdmin(admin.ModelAdmin):
    form = FeatureForm
    fieldsets = [
        (None,                {'fields': [('service',), ]}),
        ('Linked to',           {'fields': [('package', 'offer'), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]
    save_on_top = True

class PaymentAdmin(admin.ModelAdmin):
    form = PaymentForm
    fieldsets = [
        (None,                {'fields': [('feature', 'offer'), ]}),
        ('Pricing options',   {'fields': [('period', 'price'), 'term_of_usage']}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]
    save_on_top = True
    list_display = ('name', 'feature', 'offer', 'period', 'term_of_usage')
    def name(self, instance):
        return instance.__str__()
    name.short_description = 'Name'

class PeriodAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,                {'fields': [('name', 'num_of_days'), ]}),
        ('Periods',           {'fields': [('from_time', 'to_time'),]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]
    list_display = ('name', 'num_of_days', 'from_time', 'to_time')
    save_on_top = True

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'included_in')

class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    fieldsets = [
        (None,                {'fields': [('name', 'is_displayed'), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]
    save_on_top = True

# todo-me: create customized representations of Services and Directions
class DirectionsInline(admin.TabularInline):
    model = Direction

class ServicesAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'direction')
    fieldsets = [
        (None,                {'fields': ['name', ]}),
        ('Reference Info',    {'fields': [('service_type', 'direction'), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]
    # inlines = [DirectionsInline,]
    save_on_top = True

class OperatorAdmin(admin.ModelAdmin):
    form = SmallLinkForm
    list_display = ('name', 'location', 'description')
    fieldsets = [
        (None,                {'fields': [('name', 'link')]}),
        ('Location Info',     {'fields': [('location', ), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]
    inlines = [OperatorPackageInline,]
    save_on_top = True

class PackageAdmin(admin.ModelAdmin):
    form = SmallLinkForm
    list_display = ('name', 'description', 'operator', 'package_type', 'po_term', 'price')
    fieldsets = [
        (None,                {'fields': [('name', 'link')]}),
        ('Operator Info',     {'fields': [('operator', 'package_type', ), ]}),
        ('Payment Info',      {'fields': [('po_term', 'price', ), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]
    inlines = [PackageOfferInline,]
    save_on_top = True

# class FeatureAdmin(admin.ModelAdmin):
#      list_display = ('name','description', 'link')

class ParamAdmin(admin.ModelAdmin):
    list_display = ('name', 'attr', 'value', 'feature')
    fieldsets = [
        (None,                {'fields': [('attr', 'value'), ]}),
        ('Linked to',         {'fields': [('feature', ), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]
    inline = [DirectionsInline]
    save_on_top = True

class TermsOfUsageAdmin(admin.ModelAdmin):
    list_display = ('name', 'criterion', 'amount', 'unit')
    fieldsets = [
        (None,                {'fields': [('criterion', 'amount', 'unit'), ]}),
        ('Linked to',         {'fields': ['service_type', ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]
    save_on_top = True

class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'unit')
    fieldsets = [
        (None,                {'fields': [('service_type', 'name', 'unit'), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]
    save_on_top = True

class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit', 'compared_to', 'multiplier')
    fieldsets = [
        (None,                {'fields': [('name', 'unit'), ]}),
        ('Self reference',    {'fields': [('compared_to', 'multiplier'), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]
    inline = [DirectionsInline]
    save_on_top = True

class CriterionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    fieldsets = [
        (None,                {'fields': [('name', ), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]
    save_on_top = True

class DirectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'from_location', 'to_location', 'to_operator')
    fieldsets = [
        (None,                {'fields': [('from_location', 'to_location', ), ]}),
        ('Linked to',    {'fields': [('to_operator', ), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]
    save_on_top = True

class CodeAdmin(admin.ModelAdmin):
    list_display = ('operator_code', 'operator')

# todo-me: create customized representations of Offers-Features and Features-Params
admin.site.register(Direction, DirectionAdmin)
admin.site.register(ServiceType,ServiceTypeAdmin)
admin.site.register(Location,LocationAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Service, ServicesAdmin)
admin.site.register(Operator, OperatorAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Offer, OfferAdmin)
admin.site.register(Param, ParamAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Period, PeriodAdmin)
admin.site.register(POTerm)
admin.site.register(Criterion, CriterionAdmin)
admin.site.register(TermOfUsage, TermsOfUsageAdmin)#TODO is not displayed
admin.site.register(LocationType)
admin.site.register(PackageType)
admin.site.register(Directory)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Code, CodeAdmin)

