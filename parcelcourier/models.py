from django.db import models
from django_countries.fields import CountryField

# Create your models here.
STATUS_CHOICES = (
    ('awaiting payment', 'AWAITING PAYMENT'),
    ('consignment booked', 'CONSIGNMENT BOOKED'),
    (' delivery scheduled', 'DELIVERY SCHEDULED'),
    ('customs clearance', 'CUSTOMS CLEARANCE'),
    ('delay. temporary volume surge', 'DELAY. TEMPORARY VOLUME SURGE'),
    ('collected by customer at office', 'COLLECTED BY CUSTOMER AT OFFICE' )

)


class ShippingDetails(models.Model):
    tracking_number = models.IntegerField(blank=True, null=True)
    weight_in_kg = models.IntegerField()
    length_in_cm = models.IntegerField()
    height_in_cm = models.IntegerField()
    width_in_cm = models.IntegerField()
    name_of_shipper = models.CharField(max_length=500)
    Recievers_name = models.CharField(max_length=500)
    product = models.CharField(max_length=500)
    Origin = CountryField()
    Destination = CountryField()
    Departure_time = models.TimeField(blank=True, null=True)
    departure_date = models.DateField(blank=True, null= True)
    pickup_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default = 'awaiting payment', blank=True, null=True)

    def __str__(self) -> str:
        return str(self.tracking_number)
    

