__author__ = 'Kostiantyn Bezverkhyi'

from django.contrib import admin

from .models import *

# class OfferInline(admin.TabularInline):
#     model = Offer
#     fk_name = 'package'
#     # raw_id_fields = ('emp_id', 'manager_id')
#     fieldsets = [(None, {'fields': ['payment', 'package', 'po_term', 'link']}),]
#     extra = 0

class PackageInline(admin.TabularInline):
    model = Package
    fk_name = 'package'
    # raw_id_fields = ('emp_id', 'manager_id')
    fieldsets = [(None, {'fields': ['name', 'package_type', 'price', 'link']}),]
    extra = 0

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name','description','included_in')

class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name','description')

# todo-me: create customized representations of Services and Directions
class DirectionsInline(admin.TabularInline):
    model = Direction

class ServicesAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name','description']}),
        ('Reference Info', {'fields': ['service_type','direction']}),
    ]
    inline = [DirectionsInline]
    list_display = ('name', 'description','service_type','direction')

#admin.site.register(Services)
class OperatorAdmin(admin.ModelAdmin):
    list_display = ('name','description')
    inline = [PackageInline]

class PackageAdmin(admin.ModelAdmin):
    list_display = ('name','description', 'price', 'operator', 'link')
    # inlines = [OfferInline]

class ParamAdmin(admin.ModelAdmin):
    list_display = ('attr','value', 'feature')

class CodeAdmin(admin.ModelAdmin):
    list_display = ('operator_code','operator')

class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name','description', 'service_type')

# todo-me: create customized representations of Offers-Features and Features-Params
admin.site.register(Direction)
admin.site.register(ServiceType,ServiceTypeAdmin)
admin.site.register(Location,LocationAdmin)
admin.site.register(Package, PackageAdmin)
admin.site.register(Service, ServicesAdmin)
admin.site.register(Operator, OperatorAdmin)
admin.site.register(Feature)
admin.site.register(Offer)
admin.site.register(Param, ParamAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(Payment)
admin.site.register(Period)
admin.site.register(POTerm)
admin.site.register(Criterion)
admin.site.register(TermOfUsage)
admin.site.register(LocationType)
admin.site.register(PackageType)
admin.site.register(Directory)
admin.site.register(Code, CodeAdmin)

