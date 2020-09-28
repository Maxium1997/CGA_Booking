from django.db import models
from django.contrib.auth.models import AbstractUser

from registration.definition import Gender, Privilege, Identity
from rank.models import Service, Branch, MilitaryService, MilitaryBranch, Rank
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

    def get_full_name(self):
        return self.last_name + self.first_name


class Officer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    serve_state = models.PositiveSmallIntegerField(null=True)
    military_service_state = models.PositiveSmallIntegerField(null=True)
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True)
    military_service = models.ForeignKey(MilitaryService, on_delete=models.SET_NULL, null=True)
    military_branch = models.ForeignKey(MilitaryBranch, on_delete=models.SET_NULL, null=True)
    rank = models.ForeignKey(Rank, on_delete=models.SET_NULL, null=True)
    level = models.PositiveSmallIntegerField(default=1, null=True, blank=True)
    date_of_enlist = models.DateField(null=True)
    date_of_retire = models.DateField(null=True)
    attachment_of_military_ID_card_front = models.ImageField(upload_to='user', null=True, blank=True)
    attachment_of_military_ID_card_back = models.ImageField(upload_to='user', null=True, blank=True)
    attachment_of_badge_front = models.ImageField(upload_to='user', null=True, blank=True)
    attachment_of_badge_back = models.ImageField(upload_to='user', null=True, blank=True)
    identity_authentication = models.BooleanField(default=False)
    serve_record = models.TextField(null=True, blank=True)

    def attachment_of_military_ID_card_front_upload(self, photo):
        self.attachment_of_military_ID_card_front.save(self.user.username+'/officer/military-ID-card-front-{}'.format(photo),
                                                       photo,
                                                       save=True)
        self.save()

    def attachment_of_military_ID_card_back_upload(self, photo):
        self.attachment_of_military_ID_card_back.save(self.user.username+'/officer/military-ID-card-back-{}'.format(photo),
                                                      photo,
                                                      save=True)
        self.save()

    def attachment_of_badge_front_upload(self, photo):
        self.attachment_of_badge_front.save(self.user.username+'/officer/badge-front-{}'.format(photo),
                                            photo,
                                            save=True)
        self.save()

    def attachment_of_badge_back_upload(self, photo):
        self.attachment_of_badge_back.save(self.user.username+'/officer/badge-back-{}'.format(photo),
                                           photo,
                                           save=True)
        self.save()


class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    started_date = models.DateField()
    finished_date = models.DateField()

    def get_year(self):
        return self.finished_date.year


class Education(Experience):
    class_name = models.CharField(max_length=20, null=False, blank=False)


class Work(Experience):
    position = models.CharField(max_length=20, null=False, blank=False)
