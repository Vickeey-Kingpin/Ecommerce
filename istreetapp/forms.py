from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_OPTIONS = (
    ('P','Paypal'),
    ('M','Mpesa')
)

class CheckoutForm(forms.Form):
    shipping_home = forms.CharField(required=False)
    shipping_apartment = forms.CharField(required=False)
    shipping_country = CountryField(blank_label='Shipping Country').formfield(required=False,
            widget=CountrySelectWidget(attrs={
            'class': 'country'}))
    shipping_region = forms.CharField(required=False)
    use_default_shipping = forms.BooleanField(required=False)
    set_dafault_shipping = forms.BooleanField(required=False)
    shipping_same_billing = forms.BooleanField(required=False)

    billing_home = forms.CharField(required=False)
    billing_apartment = forms.CharField(required=False)
    billing_country = CountryField(blank_label='Billing Country').formfield(required=False,
            widget=CountrySelectWidget(attrs={
            'class':'country'}))
    billing_region = forms.CharField(required=False)
    use_default_billing = forms.BooleanField(required=False)
    set_dafault_billing = forms.BooleanField(required=False)

    payment_option = forms.ChoiceField(widget=forms.RadioSelect,choices=PAYMENT_OPTIONS)

class MpesaForm(forms.Form):
    phone_number = forms.CharField(required=True)