__author__ = 'Kostiantyn Bezverkhyi'

from django.db import models

class CommonInfo(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank = True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Code(models.Model):
    operator_code = models.CharField(max_length=10)
    operator_id = models.ForeignKey('Operator', related_name = 'code')
    def __str__(self):
        return self.operator_code

class Operator(CommonInfo):
    #todo-me: name field should be unique for operator
    location_id = models.ForeignKey('Location',verbose_name="Location")
    link = models.TextField(blank=True)
    class Meta:
        unique_together = (("name","location_id"),)

class Package(CommonInfo):
    price = models.DecimalField("Initial price", max_digits=7, decimal_places=2, default=0)
    operator_id = models.ForeignKey('Operator', related_name='package', verbose_name="Operator")
    package_type_id = models.ForeignKey('PackageType', verbose_name= 'Package Type')
    po_term_id = models.ForeignKey('POTerm', verbose_name='Package/Offer Term', null = True)
    link = models.TextField(blank=True)
    class Meta:
        unique_together = (("name", "operator_id"),)

class PackageType(CommonInfo):
    pass

class Offer(CommonInfo):
    payment_id = models.ForeignKey('Payment', verbose_name="Payment")
    package_id = models.ManyToManyField(Package, verbose_name="Package")
    po_term_id = models.ForeignKey('POTerm', verbose_name='Package/Offer Term')
    link = models.TextField(blank=True)

class POTerm(models.Model):
    active_from_date = models.DateField(blank=True)
    active_to_date = models.DateField(blank=True)
    order_from_date = models.DateField(blank=True)
    order_to_date = models.DateField(blank=True)
    is_active = models.IntegerField(default=1)
    def __str__(self):
        return 'Active from  %s to %s' % (self.active_from_date, self.active_to_date)

class Period(CommonInfo):
    #todo-me: chech variant with using DurationField type for remresenting period in days
    num_of_days = models.IntegerField("Number of days for period")
    #fields from_time and to_time represent information about period of time, when this offer or feature are working. For example: internet only during night hours
    from_time = models.DateTimeField(blank=True)
    to_time = models.DateTimeField(blank=True)

class Payment(models.Model):
    price = models.DecimalField("Price", max_digits=7, decimal_places=2, default=0)
    period_id = models.ForeignKey('Period')
    #todo-me Ticket:  [DataBase] Add rule for required only one field from couple #38
    feature_id = models.ForeignKey('Feature', related_name='payment',null=True)
    offer_id = models.ForeignKey('Offer', related_name='payment', null=True)
    def __str__(self):
        return 'Price of %s:%s for %s period' % (self.offer_id, self.feature_id, self.period_id)

#This table represents possible terms of using some feature/offer. For example: 10 first minutes for one price, 11 and next minutes have another price
class TermOfUsage(models.Model):
    period_id = models.ForeignKey(Period, verbose_name="Period")
    amount = models.IntegerField("Amount of minutes/message/Mbits")
    criterion_id = models.ForeignKey('Criterion', verbose_name="Criterion")

    offer_id = models.ForeignKey('Offer', verbose_name="Offer", null=True)
    feature_id = models.ForeignKey('Package', verbose_name="Package", null=True)
    def __str__(self):
        return 'Price of %s:%s for %s period' % (self.offer_id, self.feature_id, self.period_id)

#This table represent information about possible criteria: >, >=, =, <=, <
class Criterion(CommonInfo):
    pass

class LocationType(CommonInfo):
    pass

class Location(CommonInfo):
    included_in = models.ForeignKey('self', null=True, blank = True, verbose_name="Included in Location")
    location_type_id = models.ForeignKey('LocationType', verbose_name="Location Type")
    class Meta:
       unique_together = (("name"  ,"included_in"),)

class ServiceType(CommonInfo):
    #todo-me: name field should be unique for operator
    pass

class Direction(models.Model):
    from_location_id = models.ForeignKey('Location', related_name="from_directions", verbose_name="From Location")
    to_location_id = models.ForeignKey('Location', related_name="to_directions", null = True, verbose_name="To Location")
    to_operator_id = models.ForeignKey('Operator',verbose_name="To Operarot")
    def __str__(self):
        return '%s -> %s' % (self.from_location_id, self.to_location_id)
    class Meta:
        unique_together = (("from_location_id","to_location_id"),)

class Service(CommonInfo):
    service_type_id = models.ForeignKey('ServiceType', verbose_name="Service Type")
    direction_id = models.ForeignKey('Direction', verbose_name="Direction")
    class Meta:
        unique_together = (("service_type_id", "direction_id"),)

class Feature(models.Model):
    #todo-me Ticket: [DataBase] Add rule for required only one field from couple #38
    offer_id = models.ForeignKey(Offer, verbose_name="Offer", null = True)
    package_id = models.ForeignKey(Package, verbose_name="Package", null = True)
    service_id = models.ForeignKey(Service, verbose_name="Service")
    #todo-me Need to change next method. In current example only package_id or offer_id will be populated
    def __str__(self):
        return '%s:%s - %s' % (self.package_id, self.offer_id, self.service_id)
    class Meta:
        unique_together = (("offer_id","service_id"),)

class Attribute(CommonInfo):
    service_type_id = models.ForeignKey(ServiceType, verbose_name="Service Type")
    class Meta:
        unique_together = (("service_type_id","name"),)

class Param(models.Model):
    attr_id = models.ForeignKey(Attribute, verbose_name="Attribute")
    value = models.CharField(max_length=500, blank = True)
    feature_id = models.ForeignKey('Feature', verbose_name="Feature")
    def __str__(self):
        return self.attr_id

class Directory(models.Model):
    key = models.CharField(max_length=200)
    value = models.TextField()
    changed_date = models.DateTimeField(auto_now=True)