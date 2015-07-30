__author__ = 'Kostiantyn Bezverkhyi'

from django.contrib import admin

from .models import *

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name','description','is_primary','included_in')
admin.site.register(Location,LocationAdmin)

class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name','description','is_primary')
admin.site.register(ServiceType,ServiceTypeAdmin)

# todo-me: create customized representations of Services and Directions
class DirectionsInline(admin.TabularInline):
    model = Direction

class ServicesAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name','description']}),
        ('Reference Info', {'fields': ['service_type_id','direction_id']}),
    ]
    inline = [DirectionsInline]
    list_display = ('name', 'description','service_type_id','direction_id')

admin.site.register(Service, ServicesAdmin)

#admin.site.register(Services)
admin.site.register(Direction)

class OperatorAdmin(admin.ModelAdmin):
    list_display = ('name','description')
admin.site.register(Operator, OperatorAdmin)

class PackageAdmin(admin.ModelAdmin):
    list_display = ('name','description', 'price', 'operator_id')
admin.site.register(Package, PackageAdmin)

# todo-me: create customized representations of Offers-Features and Features-Params
admin.site.register(Feature)
admin.site.register(Offer)
admin.site.register(Param)

#create some specific way to populate this table
#admin.site.register(Attributes)