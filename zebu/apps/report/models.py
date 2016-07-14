from __future__ import unicode_literals

from django.db import models

# Create your models here.
class ReportTable(models.Model):
    product = models.CharField(max_length=50)
    spm = models.CharField(max_length=50)
    daily_reporter = models.CharField(max_length=50)
    file_link = models.TextField()
    is_daily_report = models.CharField(max_length= 20, default="true")

class ResourceUsageTable(models.Model):
    product = models.CharField(max_length=50)
    spm = models.CharField(max_length=50)
    daily_reporter = models.CharField(max_length=50)
    total = models.IntegerField(null = True)
    power_management = models.IntegerField(null = True)
    performance = models.IntegerField(null = True)
    function = models.IntegerField(null = True)
    zebu_platform = models.IntegerField(null = True)
    is_show=models.CharField(max_length= 20, default="true")
    power_management_str = models.CharField(max_length=100, null=True)
    performance_str = models.CharField(max_length=100, null=True)
    function_str = models.CharField(max_length=100, null=True)
    zebu_platform_str = models.CharField(max_length=100, null=True)

class ResourceUsageTitleTable(models.Model):
    total=models.IntegerField(default=0)
    usage=models.IntegerField(default=0)

class MaintfstatusTable(models.Model):
    product = models.CharField(max_length=50)
    spm = models.CharField(max_length=50)
    daily_reporter = models.CharField(max_length=50)
    is_maintf = models.CharField(max_length= 20, default="true")

class ScheduleTable(models.Model):
    product = models.CharField(max_length=50)
    spm = models.CharField(max_length=50)
    daily_reporter = models.CharField(max_length=50)
    file_link = models.TextField(null=True)
    is_schedule = models.CharField(max_length=20, default="true")
    is_picture = models.CharField(max_length=20, default="false")