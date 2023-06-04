from django.db import models
from django_countries.fields import CountryField
import random
from django.contrib.auth.models import User
# Create your models here.
STATUS_CHOICES = (
    ('awaiting payment', 'AWAITING PAYMENT'),
    ('consignment booked', 'CONSIGNMENT BOOKED'),
    (' delivery scheduled', 'DELIVERY SCHEDULED'),
    ('customs clearance', 'CUSTOMS CLEARANCE'),
    ('delay. temporary volume surge', 'DELAY. TEMPORARY VOLUME SURGE'),
    ('collected by customer at office', 'COLLECTED BY CUSTOMER AT OFFICE' )

)

DELIVERY_CHOICES = (
    ('food', 'FOOD'),
    ('phones', 'PHONES'),
    ('computer accessories', 'COMPUTER ACCESSORIES'),
    ('miscellaneous', 'MISCELLANEOUS')
)


class ShippingDetails(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    tracking_number = models.IntegerField(blank=True, null=True)
    customer_name = models.CharField(max_length=200)
    pickup_phone_number = models.IntegerField()
    pickup_address = models.CharField(max_length=200)
    recipient_name = models.CharField(max_length=200)
    recipient_phone_number = models.IntegerField()
    recipient_address = models.CharField(max_length=200)
    category= models.CharField(max_length=200, choices=DELIVERY_CHOICES, default = 'food')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default = 'awaiting payment', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.tracking_number:
            self.tracking_number = random.randint(100000, 999999)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return str(self.tracking_number)
    

