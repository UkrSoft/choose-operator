__author__ = 'Kostiantyn Bezverkhyi'

from django.db import models

class Operator(models.Model):
    name = models.CharField(primary_key=True, max_length=200)
    description = models.TextField(blank = True)
    def __str__(self):
        return self.name

class Package(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank = True)
    price = models.DecimalField("Initial price", max_digits=7, decimal_places=2, default=0)
    operator_id = models.ForeignKey(Operator, related_name='packages', verbose_name="Operator")
    def __str__(self):
        return self.name
    class Meta:
        unique_together = (("name", "operator_id"),)

class Offer(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank = True)
    price = models.DecimalField("Initial price", max_digits=7,decimal_places=2,default=0)
    package_id = models.ManyToManyField(Package, verbose_name="Package")
    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank = True)
    is_primary = models.IntegerField("Is location Primary?", default = 0)
    included_in = models.ForeignKey('self', null=True, blank = True, verbose_name="Included in Location")
    def __str__(self):
        return self.name
    class Meta:
        unique_together = (("name","included_in"),)

class ServiceType(models.Model):
    name = models.CharField(primary_key=True, max_length=200)
    description = models.TextField(blank = True)
    is_primary = models.IntegerField("Is service type Primary", default = 0)
    def __str__(self):
        return self.name

class Direction(models.Model):
    from_location_id = models.ForeignKey(Location, related_name="from_location_id", verbose_name="From Location")
    to_location_id = models.ForeignKey(Location, related_name="to_location_id", blank = True, verbose_name="To Location")
    def __str__(self):
        return '%s -> %s' % (self.from_location_id, self.to_location_id)
    class Meta:
        unique_together = (("from_location_id","to_location_id"),)

class Service(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank = True)
    service_type_id = models.ForeignKey(ServiceType, verbose_name="Service Type")
    direction_id = models.ForeignKey(Direction, verbose_name="Direction")
    def __str__(self):
        return self.name
    class Meta:
        unique_together = (("service_type_id", "direction_id"),)

class Feature(models.Model):
    offer_id = models.ForeignKey(Offer, verbose_name="Offer", null = True)
    package_id = models.ForeignKey(Package, verbose_name="Package", null = True)
    operator_id = models.ForeignKey(Operator, verbose_name="Operator", null = True)
    service_id = models.ForeignKey(Service, verbose_name="Service")
    price = models.DecimalField("Feature price",max_digits=7,decimal_places=2,default=0)
    period = models.IntegerField("Period of service", blank = True, null = True)
    num_of_min = models.IntegerField("Number of minutes for call", blank = True, null = True)
    num_of_mess = models.IntegerField("Number of messages", blank = True, null = True)
    topBand = models.IntegerField("Maximum bandwidth", blank = True, null = True)
    traffic = models.IntegerField("Number of megabytes",blank = True, null = True)
    def __str__(self):
        return '%s - %s' % (self.offer_id, self.service_id)
    class Meta:
        unique_together = (("offer_id","service_id"),)

class Attribute(models.Model):
    service_type_id = models.ForeignKey(ServiceType, verbose_name="Service Type")
    name = models.CharField(max_length=200)
    description = models.TextField(blank = True)
    def __str__(self):
        return self.name
    class Meta:
        unique_together = (("service_type_id","name"),)

class Param(models.Model):
    attr_id = models.ForeignKey(Attribute, verbose_name="Attribute")
    value = models.TextField(blank = True)
    feature_id = models.ForeignKey(Feature, verbose_name="Feature")
    def __str__(self):
        return self.attr_id
    class Meta:
        unique_together = (("attr_id","feature_id"),)