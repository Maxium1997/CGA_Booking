from datetime import datetime, timedelta
from django.db import models
from django.urls import reverse

from registration.models import User
# Create your models here.


class Proclamation(models.Model):
    title = models.CharField(max_length=20, null=False, blank=False)
    content = models.TextField()
    is_public = models.BooleanField(default=True)

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_read = models.BooleanField(default=False)

    created_time = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='announcer')
    updated_time = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updater')

    class Meta:
        ordering = ('-created_time',)

    def __str__(self):
        return self.title

    def is_new(self):
        return True if self.updated_time - datetime.now() < timedelta(days=3) else False

    def get_absolute_url(self):
        return reverse('proclamation_index')
