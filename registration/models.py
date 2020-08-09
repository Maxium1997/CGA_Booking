from django.db import models
from django.contrib.auth.models import AbstractUser

from registration.definition import Gender, Privilege
from rank.models import Rank
# Create your models here.


class User(AbstractUser):
    ID_Number = models.CharField(primary_key=True, max_length=15, null=False, blank=False, unique=True)
    gender = models.PositiveSmallIntegerField(default=Gender.Unset.value[0])
    privilege = models.PositiveSmallIntegerField(default=Privilege.User.value[0])
    identity = models.PositiveSmallIntegerField(null=False, blank=False)
    phone_Number = models.CharField(unique=True, max_length=15, null=True, blank=True)
    birthday = models.DateField(auto_now=False, null=True, blank=True)
    update_time = models.DateField(auto_now=True)


class Officer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    service_state = models.PositiveSmallIntegerField()
    rank = models.ForeignKey(Rank, on_delete=models.PROTECT)
    level = models.PositiveSmallIntegerField(default=1, null=False, blank=False)