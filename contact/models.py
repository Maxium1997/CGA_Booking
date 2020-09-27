from django.db import models

# Create your models here.


class Contact(models.Model):
    email = models.EmailField()
    phone = models.CharField()
    content = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
