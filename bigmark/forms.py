from django import forms

class CheckoutForm(forms.Form):
    street_address = forms.CharField()
    apartment = forms.CharField(required=False)