from django.db import models

# Create your models here.


class Rank(models.Model):
    name = models.CharField(max_length=10, null=False, blank=False, unique=True)
    slug = models.SlugField(max_length=155, null=False, blank=False)

    def __str__(self):
        return self.name
