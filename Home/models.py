from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Hotels(models.Model):

    options = (("single","single"),("double","double"),("suite","suite"),("dormetory","dormetory"))
    Hotel_Name = models.CharField(max_length=255)
    Room_Category = models.CharField(max_length=255,choices=options)
    Address = models.CharField(max_length=255)
    Destination_Near = models.CharField(max_length=255,null=True,blank=True)
    Aminities = models.CharField(max_length=255)
    Price = models.FloatField()
    description = models.CharField(max_length = 1000)
    Hotel_pic = models.FileField(upload_to="HOTel_pic") 
    availability = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE,null= True)


class HotelBooking(models.Model):
    Hotel = models.ForeignKey(Hotels, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    booker_Name = models.CharField(max_length=255)
    booker_phone = models.CharField(max_length=255)
    booker_address = models.CharField(max_length=255)
    booking_date = models.DateField(auto_now_add=False)
    special_Requests = models.CharField(max_length = 255,null = True)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=255)


