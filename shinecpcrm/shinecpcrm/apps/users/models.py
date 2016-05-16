from __future__ import unicode_literals

from django.db import models

# Create your models here.

# from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser


class MyUser(AbstractUser):
    name = models.CharField(max_length=50)
    empid = models.CharField(max_length=10, unique=True)
    phoneno = models.CharField(max_length=10)
    report = models.BooleanField(default=True)
    role = models.CharField(max_length=20)
    created_by = models.ForeignKey("MyUser", blank=True, null=True)

    def __unicode__(self):
        return self.first_name
