#coding:utf-8
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
                    ('classify6', 'Platform'),
                    ('classify7', 'Other')
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
                 ('module11', 'GSP'),
                 ('module12', 'Other'),
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

#is_plan标记是否在plan页显示：true是显示，false是不显示；
#is_maintf标记是否在Report的Main TF Status页显示：true是显示，false是不显示；
#is_high标记是否是Main TF Status页的Hightlight：true为是，false为不是；
#is_low标记是否是Main TF Status页的lowlight：true为是，false为不是；
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
    isdelay = models.CharField(max_length=50, default="no")
    progress = models.TextField(blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    is_plan = models.CharField(max_length= 20, default="false")
    daily_duration = models.CharField(max_length=100, null=True)
    close_time = models.DateTimeField(null=True, blank=True)
    acceptance = models.CharField(max_length= 20, default="No", choices = acceptance_choice)
    is_maintf = models.CharField(max_length=20, default="false")
    is_high = models.CharField(max_length=20, default="false")
    is_low = models.CharField(max_length=20, default="false")
    next_target=models.TextField(blank=True)

#TotalTable内容是plan页每条记录每天的daily_duration值和状态
class TotalTable(models.Model):
    change_date = models.DateField()
    daily_duration = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=50,null=True )
    request = models.ForeignKey(RequestTable, on_delete=models.CASCADE, related_name='RequestTable', null=True)

