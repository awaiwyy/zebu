from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
'''
@python_2_unicode_compatible
class users(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    #common or admin
    type = models.CharField(max_length=20)
    
    def __str__(self):
        return self.username
'''
class projectInfo(models.Model):
    project = models.CharField(max_length = 200, null=True)
    spm = models.CharField(max_length = 200, null=True)
    zebu = models.IntegerField()
    display = models.CharField(max_length= 20, default="true")

class scheduleInfo(models.Model):
    sdate = models.DateField()
    total = models.IntegerField()
    used = models.IntegerField()
    arrangement = models.CharField(max_length = 200)
    time = models.CharField(max_length = 50)
    project = models.ForeignKey(projectInfo, on_delete=models.CASCADE, related_name='projectInfo', null=True)

