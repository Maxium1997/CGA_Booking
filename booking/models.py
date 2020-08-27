from django.db import models

from registration.models import User
from registration.definition import Gender
from room.models import Room
from booking.definition import Use, State
# Create your models here.


class Booking(models.Model):
    unit_of_applicant = models.CharField(max_length=50, null=False, blank=False)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    use = models.PositiveSmallIntegerField(default=Use.OfficialBusiness.value[0])
    check_in_time = models.DateTimeField(null=False, blank=False)
    check_out_time = models.DateTimeField(null=False, blank=False)
    state = models.PositiveSmallIntegerField(default=State.Outstanding.value[0])
    booked_room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    created_time = models.DateTimeField(auto_now_add=True)
    total_price = models.PositiveIntegerField(default=0, null=False)


class Guest(models.Model):
    booking_source = models.ForeignKey(Booking, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    rank = models.CharField(max_length=155, null=True, blank=True)
    relationship = models.CharField(max_length=155, null=True, blank=True)
    ID_Number = models.CharField(max_length=15, null=False)
    gender = models.CharField(max_length=4, default=Gender.Male.value[2])
    date_of_birth = models.DateField(auto_now=False)
    phone = models.CharField(max_length=20, null=False)
    license_plate = models.CharField(max_length=10, null=True)
