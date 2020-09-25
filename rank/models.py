from django.db import models

# Create your models here.


class Service(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    slug = models.SlugField(max_length=155, null=False, blank=False)

    def __str__(self):
        return self.name


class Branch(models.Model):
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    name = models.CharField(max_length=50, null=False, blank=False, unique=True)
    slug = models.SlugField(max_length=155, null=False, blank=False)

    def __str__(self):
        return self.name


class MilitaryService(models.Model):
    name = models.CharField(max_length=10, null=False, blank=False, unique=True)
    slug = models.SlugField(max_length=155, null=False, blank=False)

    def __str__(self):
        return self.name


class MilitaryBranch(models.Model):
    military_service = models.ForeignKey(MilitaryService, on_delete=models.PROTECT)
    name = models.CharField(max_length=10, null=False, blank=False)
    slug = models.SlugField(max_length=155, null=False, blank=False)

    def __str__(self):
        return self.name


class Rank(models.Model):
    equivalent_NATO_code = models.CharField(max_length=10, default='')
    military_service = models.ForeignKey(MilitaryService, on_delete=models.PROTECT, default=None)
    name = models.CharField(max_length=10, null=False, blank=False)
    slug = models.SlugField(max_length=155, null=False, blank=False)

    def __str__(self):
        return self.name
