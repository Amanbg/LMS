from __future__ import unicode_literals

from django.db import models


from leads.models import Lead
# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=20)
    status = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    sub_category = models.CharField(max_length=20)
    lead = models.ForeignKey(Lead)

    class Meta:
        unique_together = (('category_name', 'sub_category'),)

    def __unicode__(self):
        return self.category_name
