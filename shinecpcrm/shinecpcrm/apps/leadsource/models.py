from __future__ import unicode_literals

from django.db import models

# Create your models here.


class LeadSource(models.Model):
    source_name = models.CharField(max_length=20)
    status = models.BooleanField(default=True)

    def __unicode__(self):
        return self.source_name
