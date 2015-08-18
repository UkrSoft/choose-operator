from django.core.urlresolvers import NoReverseMatch, reverse
from django.utils.safestring import mark_safe
from BestOperator.funcs import get_absolute_url

__author__ = 'Kostiantyn Bezverkhyi'

from django.db import models

class EmptyModel(models.Model):
    description = models.TextField(blank = True, help_text="Any useful information which may be helpful to easily operate current object.")
    class Meta:
        abstract = True
    # def get_admin_url(self):
    #     """
    #     Returns the admin URL to edit the object represented by this log entry.
    #     """
    #     if self._meta.app_label and self._meta.model_name:
    #         info = (self._meta.app_label, self._meta.model_name)
    #         try:
    #             return reverse('admin:%s_%s_change' % info, args=(self.pk,))
    #         except NoReverseMatch:
    #             pass
    #     return None
    # def get_absolute_url(self):
    #     return 'http://' + get_absolute_url() + self.get_admin_url()
    # def get_absolute_url_link(self):
    #     return mark_safe("<a href='%(link)s'>Click me!</a>" % {'link' : self.get_absolute_url()})

class CommonInfo(EmptyModel):
    name = models.CharField(max_length=200, help_text="Name of the current object.")
    def __str__(self):
        return self.name
    class Meta:
        abstract = True

class Code(EmptyModel):
    operator_code = models.CharField(max_length=10,
                                     help_text="Operator code - several first digits of phone number for some specific operator")
    operator = models.ForeignKey('Operator', related_name='code',
                                 help_text="Reference to operator which uses current code.")
    def __str__(self):
        return self.operator_code

class Operator(CommonInfo):
    location = models.ForeignKey('Location', verbose_name="Location",
                                 help_text="Reference to location where this operator provides services.")#TODO location could me multiple??
    link = models.TextField(blank=True, help_text="Link to the site where current operator resides.")
    class Meta:
        unique_together = (("name", "location"),)

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
    po_term = models.ForeignKey('POTerm', verbose_name='Package / Offer Term', help_text="Time term of offer usage/order")
    link = models.TextField(blank=True)
    def packages(self):
        return ", ".join(p.name for p in self.package.all())

class POTerm(EmptyModel):
    active_from_date = models.DateField(null=True, blank=True, verbose_name="Active from", help_text="Package/Offer is in service from this date")
    active_to_date = models.DateField(null=True, blank=True, verbose_name="Active to", help_text="Package/Offer is in service this this date")
    order_from_date = models.DateField(null=True, blank=True, verbose_name="Order from", help_text="Package/Offer can be bought from this date")
    order_to_date = models.DateField(null=True, blank=True, verbose_name="Order to", help_text="Package/Offer can be bought till this date")
    is_active = models.BooleanField(default=True, help_text="Is this term in use or not")
    def __str__(self):
        res_str = ""
        if self.is_active:
            res_str += "Active"
            if self.active_from_date:
                if self.active_to_date:
                    res_str += ' from %s to %s' % (self.active_from_date, self.active_to_date)
                else:
                    res_str += ' from %s' % (self.active_from_date)
            else:
                res_str += " forever"
        else:
            res_str += "Not active"
        return res_str
    class Meta:
        verbose_name = "Package / Offer Term"
        verbose_name_plural = "Package / Offer Terms"

class Period(CommonInfo):
    num_of_days = models.IntegerField("Number of days for period", null=True, blank=True, help_text="Number of day for current period.")
    from_time = models.DateTimeField(null=True, blank=True,
                                     help_text="Period of time when Offer/Feature is active. For example: from 01.00")
    to_time = models.DateTimeField(null=True, blank=True,
                                   help_text="Period of time when Offer/Feature is active. For example: to 08.00")

class Payment(EmptyModel):
    price = models.DecimalField("Price", max_digits=7, decimal_places=2, default=0, help_text="Price of Offer/Feature")
    period = models.ForeignKey('Period', null=True, blank = True, help_text="Reference to Period for current Offer/Feature")
    term_of_usage = models.ForeignKey('TermOfUsage', null=True, blank = True, help_text="Reference to Term Of Usage")
    feature = models.ForeignKey('Feature', null=True, blank=True, help_text="Reference to Feature")
    offer = models.ForeignKey('Offer', null=True, blank=True, help_text="Reference to Offer")
    def __str__(self):
        ret_str = "Price"
        if self.offer:
            ret_str += " of %(offer)s" % {'offer' : self.offer}
        if self.feature:
            ret_str += " (%(feature)s)" % {'feature' : self.feature}
        if self.period:
            ret_str += " for %(period)s" % {'period' : self.period}
        return ret_str

"""
This table represents possible terms of using some feature/offer. For example: 10 first minutes for one price, 11 and next minutes have another price
"""
class TermOfUsage(EmptyModel):
    amount = models.IntegerField("Amount", help_text="Limit to the amount of some service")
    #TODO only units for current service type should be available for selection
    unit = models.ForeignKey('Unit', verbose_name="Measurement Units", help_text="Measurement units for the amount field value.")
    criterion = models.ForeignKey('Criterion', verbose_name="Criterion",
                                  help_text="Criterion to evaluate, if == true -> use current term")
    service_type = models.ForeignKey('ServiceType', verbose_name="Service Type", help_text="Service type linked to current term")
    def __str__(self):
        return '%(criterion)s %(amount)s' % {'criterion' : self.criterion, 'amount' : self.amount}
    def name(self):
        return self.__str__()
    class Meta:
        verbose_name_plural = "Terms of Usage"

class Unit(CommonInfo):
    unit = models.CharField(max_length=200, verbose_name="Unit", help_text="Units used for measurement")
    compared_to = models.ForeignKey('self', related_name="linked_unit", null=True, blank=True, verbose_name="Compared to unit", help_text="If compare this unit to another one")
    multiplier = models.FloatField(blank=True, default=1, verbose_name="Multiply 'compared to unit'", help_text="Multiplier used to compare to values (formula is : compared_to * multiplier = unit)")
    def __str__(self):
        return self.unit

"""
Units suitable for usage by each separate service type
"""
class UnitToServiceType(CommonInfo):
    unit = models.ForeignKey('Unit', verbose_name="Unit", help_text="Units of measure")
    service_type = models.ForeignKey('ServiceType', verbose_name="Service Type", help_text="Service type linked to current term")
    def __str__(self):
        return '%s - %s' % (self.unit, self.service_type)
    class Meta:
        verbose_name_plural = "Unit to service type"

"""
This table represent information about possible criteria: >, >=, =, <=, <
"""
class Criterion(CommonInfo):
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Criteria"

class LocationType(CommonInfo):
    pass

class Location(CommonInfo):
    included_in = models.ForeignKey('self', null=True, blank=True, verbose_name="Included in Location",
                                    help_text="Reference to Location where current is included in")
    location_type = models.ForeignKey('LocationType', verbose_name="Location Type",
                                    help_text="Location type: Country, Area, Reqion etc.")
    class Meta:
       unique_together = (("name" ,"included_in"),)

class ServiceType(EmptyModel):
    name = models.CharField(max_length=200, unique = True, help_text="Name of the current object.")
    is_displayed = models.BooleanField(default=False, verbose_name="Is Displayed on Main Form", help_text="Specifies whether to display this service type on the user-inout form or not.")
    def __str__(self):
        return self.name

class Direction(EmptyModel):
    from_location = models.ForeignKey('Location', related_name="from_directions", verbose_name="From Location",
                                    help_text="Location where you use service: call, internet etc.")
    to_location = models.ForeignKey('Location', related_name="to_directions", null=True, blank=True, verbose_name="To Location",
                                    help_text="Location where you make a call, send message etc.")
    to_operator = models.ForeignKey('Operator', verbose_name="To Operarot", null=True, blank=True,
                                    help_text="Destination operator, who will receive call or message")
    def __str__(self):
        res_str = "%(from_loc)s" % {'from_loc' : self.from_location}
        if (self.to_location):
            res_str += " -> %(to_loc)s" % {'to_loc' : self.to_location}
        if (self.to_operator):
            res_str += " (%(to_oper)s)" % {'to_oper' : self.to_operator}
        return res_str
    class Meta:
        unique_together = (("from_location", "to_location", "to_operator"),)

class Service(EmptyModel):#TODO it should be possible to provide default value of name field without duplicating field from the 'CommonInfo' model: http://stackoverflow.com/questions/4904230/django-change-default-value-for-an-extended-model-class
    name = models.CharField(max_length=200, default="<auto-generated>", help_text="Name of the current object.")
    service_type = models.ForeignKey('ServiceType', verbose_name="Service Type",
                                     help_text="Service Type: call, SMS, internet etc.")
    direction = models.ForeignKey('Direction', verbose_name="Direction",
                                  help_text="Direction of the call, SMS, internet etc.")
    def save(self, *args, **kwargs):
        if self.name == '<auto-generated>':
            self.name = '%s - %s' % (self.service_type, self.direction)
        super(Service, self).save(*args, **kwargs)
    def __str__(self):
        return self.name
    class Meta:
        unique_together = (("service_type", "direction"),)

class Feature(EmptyModel):
    offer = models.ForeignKey(Offer, verbose_name="Offer", null=True, blank=True, help_text="Related Offer")
    package = models.ForeignKey(Package, verbose_name="Package", null=True, blank=True, help_text="Related Package")
    service = models.ForeignKey(Service, verbose_name="Service", help_text="Provided service in scope of this feature")
    def __str__(self):
        res_str = "%(service)s" % {'service' : self.service}
        if self.offer:
            res_str += " (offer: %(offer)s" % {'offer' : self.offer}
        if self.package:
            res_str += " " if self.offer else " ("
            res_str += "package: %(package)s " % {'package' : self.package}
        if self.offer or self.package:
            res_str += ")"
        return res_str
    class Meta:
        unique_together = (("offer", "service"),)

class Attribute(CommonInfo):
    service_type = models.ForeignKey(ServiceType, verbose_name="Service Type",
                                     help_text="Service Type that can have such attribute")
    unit = models.ForeignKey('Unit', help_text="Measurement units linked with current attribute")
    class Meta:
        unique_together = (("service_type", "name"),)

class Param(EmptyModel):
    attr = models.ForeignKey(Attribute, verbose_name="Attribute", help_text="Reference to Attribute")
    value = models.CharField(max_length=500, null = True, blank=True, help_text="Value of parameter")
    feature = models.ForeignKey('Feature', verbose_name="Feature", help_text="Reference to Feature" )
    def __str__(self):
        ret_str = "%(attr)s" % {'attr' : self.attr}
        if self.value:
            ret_str += " = %(val)s" % {'val' : self.value}
        return ret_str
    def name(self):
        return "%(feature)s - %(str)s" % {'feature' : self.feature, 'str' : self.__str__()}
    class Meta:
        verbose_name = "Parameter"
        verbose_name_plural = "Parameters"

class Directory(models.Model):
    key = models.CharField(max_length=200, help_text="Name of the key")
    value = models.TextField(help_text="Value of current key")
    changed_date = models.DateTimeField(auto_now=True, help_text="Date when current key was changed last time")
    class Meta:
        verbose_name_plural = "Directories"
