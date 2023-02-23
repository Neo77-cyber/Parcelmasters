from .models import ShippingDetails
from django import forms



class ShippingDetailsForm(forms.ModelForm):
    class Meta:
        model = ShippingDetails
        fields = ('name_of_shipper', 'Recievers_name', 'product', 'Origin', 'Destination', 'weight_in_kg', 'length_in_cm', 'height_in_cm', 'width_in_cm', )

