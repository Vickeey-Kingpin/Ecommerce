from django import forms
from django_countries.fields import CountryField


class CheckoutForm(forms.Form):
    shipping_home = forms.CharField()
    shipping_apartment = forms.CharField()
    shipping_country = CountryField().formfield()
    shipping_region = forms.CharField()
    use_default_shipping = forms.BooleanField(required=False)
    set_dafault_shipping = forms.BooleanField(required=False)
    shipping_same_billing = forms.BooleanField(required=False)

# same_billing_as_shipping
# set_as_default_shipping