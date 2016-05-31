from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
project_choice = (
                  ('prj1', 'iwhale2'),
                  ('prj2', 'other'),
                 )

classification_choice = (
                    ('classify1', 'Function'),
                    ('classify2', 'Misc'),
                    ('classify3', 'Performance'),
                    ('classify4', 'Power'),
                    ('classify5', 'Kernel'),
                    ('classify6', 'Other'),
                )

module_choice = (
                 ('module1', 'APPS'),
                 ('module2', 'BSP'),
                 ('module3', 'MM'),
                 ('module4', 'Modem'),
                 ('module5', 'Power'),
                 ('module6', 'Stability'),
                 ('module7', 'Kernel'),
                 ('module8', 'Graphics'),
                 ('module9', 'DDR'),
                 ('module10', 'WCN'),
                )

environment_choice = (
                      ('env1', 'Zebu'),
                      ('env2', 'Hybrid'),
                    )
'''
request_duration_choice = (
                           ('rq_dur1', '12H'),
                           ('rq_dur2', '24H'),
                           ('rq_dur3', '36H'),
                           ('rq_dur4', '48H'),
                           ('rq_dur5', '60H'),
                           ('rq_dur6', '72H'),
                           ('rq_dur7', '84H'),
                           ('rq_dur8', '96H'),
                           ('rq_dur9', '108H'),
                           ('rq_dur10', '120H'),
                        )
'''

tf_choice = (
             ('tf1', 'option1'),
             ('tf2', 'option2'),
            )

priority_choice = (
                   ('level1', 'High'),
                   ('level2', 'Normal'),
                   ('level3', 'Low'),
                   )

acceptance_choice = (
              ('unaccept', 'No'),
              ('accept', 'Yes'),
              )

class RequestTable(models.Model):
    project = models.CharField(max_length=100, choices = project_choice)
    classification = models.CharField(max_length=100, choices = classification_choice)
    module = models.CharField(max_length=100, choices = module_choice)
    tf_case = models.CharField(max_length = 50, choices = tf_choice)
    action_discription = models.TextField()
    environment = models.CharField(max_length=100, choices = environment_choice)
    request_duration = models.CharField(max_length=100, null=True, blank=True)
    owner = models.CharField(max_length=50)
    priority = models.CharField(max_length=100, choices = priority_choice)
    submit_date = models.DateField(auto_now_add=True)
    duration = models.CharField(max_length=50, null=True)
    status = models.CharField(max_length=50, default="wait for zebu")
    progress = models.TextField(blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    is_plan = models.CharField(max_length= 20, default="false")
    daily_duration = models.CharField(max_length=100, null=True)
    close_time = models.DateTimeField(null=True, blank=True)
    acceptance = models.CharField(max_length= 20, default="No", choices = acceptance_choice)
    