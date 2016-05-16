from __future__ import unicode_literals

from django.db import models
from leads.models import Lead
from users.models import MyUser


class Comment(models.Model):
    description = models.CharField(max_length=100)
    lead = models.ForeignKey(Lead)
    package_offered = models.CharField(max_length=100)
    created_by = models.ForeignKey(MyUser)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __unicode__(self):
        return self.description
