from .models import ShippingDetails
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User




class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']

       

class ShippingDetailsForm(forms.ModelForm):
    class Meta:
        model = ShippingDetails
        fields = ('customer_name', 'pickup_phone_number', 'pickup_address', 'recipient_name', 'recipient_phone_number', 'recipient_address', 'category')

