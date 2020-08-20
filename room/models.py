from django.db import models

from registration.models import User
# Create your models here.


class Hotel(models.Model):
    name = models.CharField(max_length=20, unique=True, null=False, blank=False)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    external_appearance = models.ImageField(upload_to='hotels', null=True, blank=True)
    slug = models.SlugField(max_length=255, unique=True, null=False, blank=False)
    address = models.CharField(max_length=50, unique=True, null=True)
    phone = models.CharField(max_length=20, unique=True, null=True)
    website = models.URLField(unique=True, null=True)
    introduction = models.TextField(null=True, blank=True)

    def photo_upload(self, photo):
        self.external_appearance.save(self.name+'/{}'.format(self.external_appearance),
                                      photo,
                                      save=True)
        self.save()

    def __str__(self):
        return self.name


class Room(models.Model):
    name = models.CharField(max_length=20, null=False, blank=False)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='hotels', null=True, blank=True)
    price = models.PositiveIntegerField(default=0, null=True, blank=True)
    single_bed = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    double_bed = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    size = models.PositiveSmallIntegerField(null=True, blank=True)

    def get_price(self):
        return self.price

    def photo_upload(self, photo):
        self.photo.save(self.hotel.name+'/{}/{}'.format(self.name, photo),
                        photo,
                        save=True)
        self.save()

    def __str__(self):
        return self.hotel.name + ' ' + self.name


class Dormitory(models.Model):
    room = models.OneToOneField(Room, on_delete=models.CASCADE)
    washing_fee = models.PositiveSmallIntegerField(default=0, null=True)
    usage_fee = models.PositiveSmallIntegerField(default=0, null=True)
    utility_bill = models.PositiveSmallIntegerField(default=0, null=True)

    def get_price(self):
        total_price = 0
        if self.room.price:
            total_price += self.room.price
        if self.washing_fee:
            total_price += self.washing_fee
        if self.usage_fee:
            total_price += self.usage_fee
        if self.utility_bill:
            total_price += self.utility_bill
        return total_price

    def __str__(self):
        return self.room.hotel.name + ' ' + self.room.name
