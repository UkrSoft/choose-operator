from django.contrib import admin

from BestOperator.forms import FeatureForm, PaymentForm
from .models import *

__author__ = 'Kostiantyn Bezverkhyi'

class FeatureAdmin(admin.ModelAdmin):
    form = FeatureForm
    fieldsets = [
        (None,                {'fields': [('service',), ]}),
        ('Linkage',           {'fields': [('package', 'offer'), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]
    save_on_top = True

class PaymentAdmin(admin.ModelAdmin):
    form = PaymentForm
    fieldsets = [
        (None,                {'fields': [('feature', 'offer'), ]}),
        ('Pricing options',   {'fields': [('period', 'price'), 'term_of_usage']}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]#TODO set custom name for the __str__ field in the admin
    list_display = ('__str__', 'feature', 'offer', 'period', 'term_of_usage')
    save_on_top = True


class FeatureInline(admin.TabularInline):
    model = Feature
    fk_name = 'offer'
    fieldsets = [(None, {'fields': ['service']}), ]
    extra = 0


class OfferInline(admin.TabularInline):
    # readonly_fields = ['selflink',]
    model = Offer.package.through  # TODO 'link' field output should be override - it is too high
    # fk_name = 'offer'
    # fieldsets = [(None, {'fields':['selflink', 'offer']}),]
    extra = 0

class PackageInline(admin.TabularInline):
    readonly_fields = ['selflink',]
    model = Package
    fk_name = 'operator'#TODO 'link' field output should be override - it is too high
    fieldsets = [(None, {'fields': ['selflink', 'name', 'package_type', 'price', 'link']}), ]
    extra = 0

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
    list_display = ('name', 'location', 'description')
    fieldsets = [
        (None,                {'fields': [('name', 'link')]}),
        ('Reference Info',    {'fields': [('location', ), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]
    inlines = [PackageInline,]
    save_on_top = True

class PackageAdmin(admin.ModelAdmin):
    list_display = ('name','description', 'price', 'operator', 'link')
    inlines = [OfferInline, ]


class OfferAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'link')
    inlines = [FeatureInline, ]


# class FeatureAdmin(admin.ModelAdmin):
#      list_display = ('name','description', 'link')

class ParamAdmin(admin.ModelAdmin):
    list_display = ('custom_name', 'attr', 'value', 'feature')
    fieldsets = [
        (None,                {'fields': [('attr', 'value'), ]}),
        ('Reference Info',    {'fields': [('feature', ), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]
    inline = [DirectionsInline]
    save_on_top = True

class UnitAdmin(admin.ModelAdmin):
    list_display = ('unit', 'compared_to', 'multiplier')
    fieldsets = [
        (None,                {'fields': [('name', 'unit'), ]}),
        ('Reference Info',    {'fields': [('compared_to', 'multiplier'), ]}),
        ('Extra',             {'fields': ['description'], 'classes':['collapse']}),
    ]
    inline = [DirectionsInline]
    save_on_top = True

class CodeAdmin(admin.ModelAdmin):
    list_display = ('operator_code', 'operator')

class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'service_type')

# todo-me: create customized representations of Offers-Features and Features-Params
admin.site.register(Direction)
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
admin.site.register(Period)
admin.site.register(POTerm)
admin.site.register(Criterion)
admin.site.register(TermOfUsage)
admin.site.register(LocationType)
admin.site.register(PackageType)
admin.site.register(Directory)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Code, CodeAdmin)

