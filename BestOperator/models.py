__author__ = 'Kostiantyn Bezverkhyi'


from django.db import models

class Operators(models.Model):
    # Type of fields will be updated after additional learning of types
    name = models.CharField(max_length=30, null=False)
    description = models.TextField(max_length=100)

class Offers(models.Model):
    name = models.CharField(max_length=30, null=False)
    description = models.TextField(max_length=100)
    price = models.DecimalField(max_digits=7,decimal_places=2,default=0)

class Packages(models.Model):
    name = models.CharField(max_length=30, null=False)
    description = models.TextField(max_length=100)
    price = models.DecimalField(max_digits=7,decimal_places=2,default=0)
    operator_id = models.ForeignKey(Operators)
    offer_id = models.ManyToManyField(Offers)

class Locations(models.Model):
    name = models.CharField(max_length=30, null=False)
    description = models.TextField(max_length=100)
    isprimary = models.IntegerField(default = 0)
    included_in = models.ForeignKey('self', null=True)

class ServiceTypes(models.Model):
    name = models.CharField(max_length=30, null=False)
    description = models.TextField(max_length=100)
    isprimary = models.IntegerField(default = 0)

class Directions(models.Model):
    from_location_id = models.ForeignKey(Locations, related_name="from_location_id")
    to_location_id = models.ForeignKey(Locations, related_name="to_location_id")

class Services(models.Model):
    name = models.CharField(max_length=30, null=False)
    description = models.TextField(max_length=100)
    service_type_id = models.ForeignKey(ServiceTypes, null=False)
    direction_id = models.ForeignKey(Directions, null=False)

class Features(models.Model):
    offer_id = models.ForeignKey(Offers)
    package_id = models.ForeignKey(Packages)
    operator_id = models.ForeignKey(Operators)
    service_id = models.ForeignKey(Services, null=False)
    price = models.DecimalField(max_digits=7,decimal_places=2,default=0)
    period = models.IntegerField()
    num_of_min = models.IntegerField()
    num_of_mess = models.IntegerField()
    topBand = models.IntegerField()
    traffic = models.IntegerField()

class Attributes(models.Model):
    service_type_id = models.ForeignKey(ServiceTypes, null=False)
    name = models.CharField(max_length=30, null=False)
    description = models.TextField(max_length=100)

class Params(models.Model):
    attr_id = models.ForeignKey(Attributes, null=False)
    value = models.TextField
    feature_id = models.ForeignKey(Features,null=False)