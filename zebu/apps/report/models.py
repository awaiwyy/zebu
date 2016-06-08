from __future__ import unicode_literals

from django.db import models

# Create your models here.
class ReportTable(models.Model):
    product = models.CharField(max_length=50)
    spm = models.CharField(max_length=50)
    daily_reporter = models.CharField(max_length=50)
    file_link = models.TextField()