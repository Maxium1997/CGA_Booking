from django.db import models
from django.contrib.auth.models import AbstractUser

from registration.definition import Gender, Privilege, Identity
from rank.models import Rank
# Create your models here.


class User(AbstractUser):
    ID_Number = models.CharField(primary_key=True, max_length=15, null=False, blank=False, unique=True)
    gender = models.PositiveSmallIntegerField(default=Gender.Unset.value[0], null=False, blank=False)
    privilege = models.PositiveSmallIntegerField(default=Privilege.User.value[0], null=False, blank=False)
    identity = models.PositiveSmallIntegerField(default=Identity.Traveler.value[0], null=False, blank=False)
    phone_number = models.CharField(unique=True, max_length=15, null=True)
    birthday = models.DateField(auto_now=False, null=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-is_superuser',)


class Officer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    service_state = models.PositiveSmallIntegerField()
    rank = models.ForeignKey(Rank, on_delete=models.PROTECT)
    level = models.PositiveSmallIntegerField(default=1, null=False, blank=False)
