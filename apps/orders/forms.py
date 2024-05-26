from django import forms
from .models import OrderModel


class PhoneVerificationForm(forms.Form):
    phone = forms.CharField(max_length=11, label='شماره تلفن')


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = OrderModel
        fields = [
            'first_name', 'last_name',
            'phone', 'address',
            'postal_code', 'province',
            'city'
        ]
