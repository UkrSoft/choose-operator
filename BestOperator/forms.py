from django import forms
from django.forms import models
from BestOperator.models import Offer, Package, Service, Feature, Payment, \
    EmptyModel


class SmallLinkForm(forms.ModelForm):
    link = forms.CharField(required=False, widget=forms.Textarea(attrs={'rows':2, 'cols':80}))
    class Meta:
        model = EmptyModel
        fields = models.ALL_FIELDS

class FeatureForm(forms.ModelForm):#TODO why help text is not displayed in the form?
    offer = forms.ModelChoiceField(queryset=Offer.objects.all(), required=False)
    package = forms.ModelChoiceField(queryset=Package.objects.all(), required=False)
    service = forms.ModelChoiceField(queryset=Service.objects.all()) #TODO this field was added to add custom widget to admin in the future
    def clean(self):
        cleaned_data = super(FeatureForm, self).clean()
        package = cleaned_data.get("package")
        offer = cleaned_data.get("offer")

        if package is None == offer is None:
            msg = "Neither package nor offer field value was specified."
            self.add_error('package', msg)
            self.add_error('offer', msg)
    class Meta:
        model = Feature
        fields = models.ALL_FIELDS

class PaymentForm(forms.ModelForm):
    offer = forms.ModelChoiceField(queryset=Offer.objects.all(), required=False)
    feature = forms.ModelChoiceField(queryset=Feature.objects.all(), required=False)
    def clean(self):
        cleaned_data = super(PaymentForm, self).clean()
        feature = cleaned_data.get("feature")
        offer = cleaned_data.get("offer")

        if feature is None == offer is None:
            msg = "Neither feature nor offer field value was specified."
            self.add_error('feature', msg)
            self.add_error('offer', msg)
    class Meta:
        model = Payment
        fields = models.ALL_FIELDS

class OfferForm(SmallLinkForm):
    package = forms.ModelMultipleChoiceField(queryset=Package.objects.all(), required=True,
                                             widget=forms.CheckboxSelectMultiple)
