from django import forms
from django.contrib import admin
from django.forms import models
from BestOperator.models import Offer, Package, Feature, Payment, \
    DescriptionModel
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.utils.translation import ugettext_lazy as _

def add_related_field_wrapper(form, col_name):
    rel = form.Meta.model._meta.get_field(col_name).rel
    form.fields[col_name].widget = RelatedFieldWidgetWrapper(
        form.fields[col_name].widget, rel, admin.site,
        can_add_related=True, can_change_related=True)

class SmallLinkForm(forms.ModelForm):
    link = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':2, 'cols':80}))
    class Meta:
        model = DescriptionModel
        fields = models.ALL_FIELDS

class FeatureForm(forms.ModelForm):#TODO why help text is not displayed?
    offer = forms.ModelChoiceField(queryset=Offer.objects.all(), required=False)
    package = forms.ModelChoiceField(queryset=Package.objects.all(), required=False)
    def __init__(self, *args, **kwargs):
        super(FeatureForm, self).__init__(*args, **kwargs)
        add_related_field_wrapper(self, 'offer')
        add_related_field_wrapper(self, 'package')
    def clean(self):
        cleaned_data = super(FeatureForm, self).clean()
        package = cleaned_data.get("package")
        offer = cleaned_data.get("offer")

        msg = None
        if package is None and offer is None:
            msg = _("Neither package nor offer field value was specified.")
        if package is not None and offer is not None:
            msg = _("Only one of package or offer fields should be populated.")
        if msg:
            self.add_error('package', msg)
            self.add_error('offer', msg)
    class Meta:
        model = Feature
        fields = models.ALL_FIELDS

class PaymentForm(forms.ModelForm):
    offer = forms.ModelChoiceField(queryset=Offer.objects.all(), required=False)
    feature = forms.ModelChoiceField(queryset=Feature.objects.all(), required=False)
    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        add_related_field_wrapper(self, 'offer')
        add_related_field_wrapper(self, 'feature')
    def clean(self):
        cleaned_data = super(PaymentForm, self).clean()
        feature = cleaned_data.get("feature")
        offer = cleaned_data.get("offer")

        msg = None
        if feature is None and offer is None:
            msg = _("Neither feature nor offer field value was specified.")
        if feature is not None and offer is not None:
            msg = _("Only one of feature or offer fields should be populated.")
        if msg:
            self.add_error('feature', msg)
            self.add_error('offer', msg)
    class Meta:
        model = Payment
        fields = models.ALL_FIELDS
