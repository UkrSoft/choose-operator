__author__ = 'Kostiantyn Bezverkhyi'

from django.contrib import admin

from .models import *

admin.site.register(Attributes)
admin.site.register(Directions)
admin.site.register(Features)
admin.site.register(Locations)
admin.site.register(Offers)
admin.site.register(Operators)
admin.site.register(Packages)
admin.site.register(Params)
admin.site.register(Services)
admin.site.register(ServiceTypes)

