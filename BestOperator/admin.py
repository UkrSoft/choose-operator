__author__ = 'Kostiantyn Bezverkhyi'

from django.contrib import admin

from .models import *

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name','description','isprimary','included_in')
admin.site.register(Location,LocationAdmin)

class ServiceTypeAdmin(admin.ModelAdmin):
    list_display = ('name','description','isprimary')
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

admin.site.register(Operator)
admin.site.register(Package)

# todo-me: create customized representations of Offers-Features and Features-Params
admin.site.register(Feature)
admin.site.register(Offer)
admin.site.register(Param)

#create some specific way to populate this table
#admin.site.register(Attributes)