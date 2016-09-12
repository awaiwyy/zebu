from __future__ import unicode_literals

from django.db import models

# Create your models here.
class ResourceTable(models.Model):
    resource_id = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    environment = models.CharField(max_length=50)