__author__ = 'Kostiantyn Bezverkhyi'

from django.db import models

class Operator(models.Model):
    # Type of fields will be updated after additional learning of types
    name = models.CharField(max_length=200)
    description = models.TextField(blank = True)

class Offer(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank = True)
    price = models.DecimalField(max_digits=7,decimal_places=2,default=0)

class Package(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank = True)
    price = models.DecimalField(max_digits=7,decimal_places=2,default=0)
    operator_id = models.ForeignKey(Operator)
    offer_id = models.ManyToManyField(Offer)

class Location(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank = True)
    isprimary = models.IntegerField(default = 0)
    included_in = models.ForeignKey('self', null=True, blank = True)

class ServiceType(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank = True)
    isprimary = models.IntegerField(default = 0)

class Direction(models.Model):
    from_location_id = models.ForeignKey(Location, related_name="from_location_id")
    to_location_id = models.ForeignKey(Location, related_name="to_location_id", blank = True)

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank = True)
    service_type_id = models.ForeignKey(ServiceType)
    direction_id = models.ForeignKey(Direction)

class Feature(models.Model):
    offer_id = models.ForeignKey(Offer)
    package_id = models.ForeignKey(Package)
    operator_id = models.ForeignKey(Operator)
    service_id = models.ForeignKey(Service)
    price = models.DecimalField(max_digits=7,decimal_places=2,default=0)
    period = models.IntegerField(blank = True)
    num_of_min = models.IntegerField(blank = True)
    num_of_mess = models.IntegerField(blank = True)
    topBand = models.IntegerField(blank = True)
    traffic = models.IntegerField(blank = True)

class Attribute(models.Model):
    service_type_id = models.ForeignKey(ServiceType)
    name = models.CharField(max_length=200)
    description = models.TextField(blank = True)

class Param(models.Model):
    attr_id = models.ForeignKey(Attribute)
    value = models.TextField(blank = True)
    feature_id = models.ForeignKey(Feature)