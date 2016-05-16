from __future__ import unicode_literals

from django.db import models
from leadsource.models import LeadSource
from users.models import MyUser

# Create your models here.


class Lead(models.Model):
    username = models.CharField(max_length=20)
    email_id = models.CharField(max_length=50)
    name = models.CharField(max_length=30)
    contact = models.CharField(max_length=10)
    city = models.CharField(max_length=20)
    experience_years = models.IntegerField(default=0)
    experience_level = models.IntegerField(default=0)
    industry = models.CharField(max_length=40)
    salary = models.IntegerField(default=0)
    source = models.ForeignKey(LeadSource)
    product_name = models.CharField(max_length=40)
    created_by = models.ForeignKey(MyUser)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True, auto_now_add=False)
    followup_time = models.DateTimeField(auto_now=True, auto_now_add=False)
    assign_date = models.DateTimeField(auto_now=False, auto_now_add=True)
    assign_to = models.ForeignKey(MyUser, related_name='assign_to')

    def __unicode__(self):
        return self.username
