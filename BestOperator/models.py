__author__ = 'Kostiantyn Bezverkhyi'

from django.db import models

class CommonInfo(models.Model):
    name = models.CharField(max_length=200, help_text="Name of the current object.")
    description = models.TextField(blank = True, help_text="Any useful information which may be used to easily operate current object.")

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Code(models.Model):
    operator_code = models.CharField(max_length=10,
                                     help_text="Operator code - several first digits of phone number for some specific operator")
    operator = models.ForeignKey('Operator', related_name='code',
                                 help_text="Reference to operator which uses current code.")
    def __str__(self):
        return self.operator_code

class Operator(CommonInfo):
    #todo-me: name field should be unique for operator
    location = models.ForeignKey('Location', verbose_name="Location",
                                 help_text="Reference to location where this operator provides services.")  # could me multiple??
    link = models.TextField(blank=True, help_text="Link to the site where current operator resides.")
    class Meta:
        unique_together = (("name","location"),)

class Package(CommonInfo):
    price = models.DecimalField("Initial price", max_digits=7, decimal_places=2, default=0, help_text="Initial price of package. Price that you pay when buy a new sim-card.")
    operator = models.ForeignKey('Operator', related_name='package', verbose_name="Operator",
                                 help_text="Reference to related Operator.")
    package_type = models.ForeignKey('PackageType', verbose_name='Package Type',
                                     help_text="Some specific Package Type: Prepayment, Contract, Business etc.")
    po_term = models.ForeignKey('POTerm', verbose_name='Package/Offer Term', null=True, blank=True,
                                help_text="Time term of package usage/order")
    link = models.TextField(blank=True, help_text="Link to the site with current package")
    class Meta:
        unique_together = (("name", "operator"),)

class PackageType(CommonInfo):
    pass

class Offer(CommonInfo):
    package = models.ManyToManyField(Package, verbose_name="Package", help_text="Reference to related package")
    po_term = models.ForeignKey('POTerm', verbose_name='Package/Offer Term', help_text="Time term of offer usage/order")
    link = models.TextField(blank=True)

class POTerm(models.Model):
    active_from_date = models.DateField(null=True, blank=True, help_text="Package/Offer is in service from this date")
    active_to_date = models.DateField(null=True, blank=True, help_text="Package/Offer is in service this this date")
    order_from_date = models.DateField(null=True, blank=True, help_text="Package/Offer can be bought from this date")
    order_to_date = models.DateField(null=True, blank=True, help_text="Package/Offer can be bought till this date")
    is_active = models.IntegerField(default=1, help_text="Decision flag. Is in use: 1; Out of use: 0")
    def __str__(self):
        return 'Active from  %s to %s' % (self.active_from_date, self.active_to_date)

class Period(CommonInfo):
    #todo-me: check variant with using DurationField type for resetting period in days
    num_of_days = models.IntegerField("Number of days for period", help_text="Number of day for current period.")
    from_time = models.DateTimeField(null=True, blank=True,
                                     help_text="Period of time whne Offer/Feature is active. For example: from 01.00")
    to_time = models.DateTimeField(null=True, blank=True,
                                   help_text="Period of time whne Offer/Feature is active. For example: to 08.00")

class Payment(models.Model):
    price = models.DecimalField("Price", max_digits=7, decimal_places=2, default=0, help_text="Price of Offer/Feature")
    period = models.ForeignKey('Period', help_text="Reference to Period for current Offer/Feature")
    #todo-me Ticket:  [DataBase] Add rule for required only one field from couple #38
    feature = models.ForeignKey('Feature', related_name='payment', null=True, blank=True, help_text="Reference to Feature")
    offer = models.ForeignKey('Offer', related_name='payment', null=True, blank=True, help_text="Reference to Offer")
    def __str__(self):
        return 'Price of %s:%s for %s period' % (self.offer, self.feature, self.period)

#This table represents possible terms of using some feature/offer. For example: 10 first minutes for one price, 11 and next minutes have another price
class TermOfUsage(models.Model):
    period = models.ForeignKey(Period, verbose_name="Period", help_text="Period of tme when Offer/Feature is in use")
    amount = models.IntegerField("Amount of minutes/message/Mbits",
                                 help_text="Amount of minutes/message/Mbits that are limited")
    criterion = models.ForeignKey('Criterion', verbose_name="Criterion",
                                  help_text="Criterion related to amount. For example: '<'. It means that such TermOfUsage for amount of min/mes that is < amount(field)")

    offer = models.ForeignKey('Offer', verbose_name="Offer", null=True, blank=True, help_text="Reference to Offer")
    feature = models.ForeignKey('Feature', verbose_name="Feature", null=True, blank=True, help_text="Reference to Package")
    def __str__(self):
        return 'Price of %s:%s for %s period' % (self.offer, self.feature, self.period)

#This table represent information about possible criteria: >, >=, =, <=, <
class Criterion(CommonInfo):
    pass

class LocationType(CommonInfo):
    pass

class Location(CommonInfo):
    included_in = models.ForeignKey('self', null=True, blank=True, verbose_name="Included in Location",
                                    help_text="Reference to Location where current is included in")
    location_type = models.ForeignKey('LocationType', verbose_name="Location Type",
                                      help_text="Location type: Country, Area, Reqion etc.")
    class Meta:
       unique_together = (("name" ,"included_in"),)

class ServiceType(CommonInfo):
    pass
    is_displayed = models.BooleanField(default=False, help_text="Configuration flag.")
    #todo-me: name field should be unique for operator
    # def save(self, *args, **kwargs):#TODO you may try overriding this method
    #         if self.name == "Yoko Ono's blog":
    #             return # Yoko shall never have her own blog!
    #         else:
    #             super(Blog, self).save(*args, **kwargs) # Call the "real" save() method.

class Direction(models.Model):
    from_location = models.ForeignKey('Location', related_name="from_directions", verbose_name="From Location",
                                      help_text="Location where you use service: call, internet etc.")
    to_location = models.ForeignKey('Location', related_name="to_directions", null=True, blank=True, verbose_name="To Location",
                                    help_text="Location where you make a call, send message etc.")
    to_operator = models.ForeignKey('Operator', verbose_name="To Operarot", null=True, blank=True,
                                    help_text="Destination operator, who will receive call or message")
    def __str__(self):
        return '%s -> %s' % (self.from_location, self.to_location)
    class Meta:
        unique_together = (("from_location","to_location"),)

class Service(CommonInfo):
    service_type = models.ForeignKey('ServiceType', verbose_name="Service Type",
                                     help_text="Service Type: call, internet, SMS etc.")
    direction = models.ForeignKey('Direction', verbose_name="Direction",
                                  help_text="Direction of the call, sms, internet(just from) etc.")
    class Meta:
        unique_together = (("service_type", "direction"),)

class Feature(models.Model):
    #todo-me Ticket: [DataBase] Add rule for required only one field from couple #38
    offer = models.ForeignKey(Offer, verbose_name="Offer", null=True, blank=True, help_text="Related Offer")
    package = models.ForeignKey(Package, verbose_name="Package", null=True, blank=True, help_text="Related Package")
    service = models.ForeignKey(Service, verbose_name="Service", help_text="Provided service in scope of this feature")
    #todo-me Need to change next method. In current example only package or offer will be populated
    def __str__(self):
        return '%s:%s - %s' % (self.package, self.offer, self.service)
    class Meta:
        unique_together = (("offer","service"),)

class Attribute(CommonInfo):
    service_type = models.ForeignKey(ServiceType, verbose_name="Service Type",
                                     help_text="Service Type that can have such attribute")
    class Meta:
        unique_together = (("service_type","name"),)

class Param(models.Model):
    attr = models.ForeignKey(Attribute, verbose_name="Attribute", help_text="Reference to Attribute")
    value = models.CharField(max_length=500, null = True, blank=True, help_text="Value of parameter")
    feature = models.ForeignKey('Feature', verbose_name="Feature", help_text="Reference to Feature" )
    def __str__(self):
        return self.attr.name

class Directory(models.Model):
    key = models.CharField(max_length=200, help_text="Name of the key")
    value = models.TextField(help_text="Value of current key")
    changed_date = models.DateTimeField(auto_now=True, help_text="Date when current key was changed last time")
