#!/usr/bin/env python
#coding:utf-8

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zebu.settings")

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
'''
Django 版本大于等于1.7的时候，需要加上下面两句
import django
django.setup()
否则会抛出错误 django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
'''

import django
if django.VERSION >= (1, 7):#自动判断版本
    django.setup()

from apps.request.models import RequestTable
from apps.newhome.models import ResourceTable
from common import sendEmail
from common import sendEmailTest
import datetime
import time
from dateutil.tz import *
def main():

    resourcetable = ResourceTable.objects.all()
    current_time=datetime.datetime.now(tzutc())
    for tab in resourcetable:
        resource=tab.resource_id
        print resource+":"
        assignedtable = RequestTable.objects.filter(assign_ID__contains=resource, assign_starttime__isnull=False,assign_endtime__gt=current_time).order_by("assign_starttime")[0:2]
        if assignedtable:
            start1=assignedtable[0].assign_starttime
            end1=assignedtable[0].assign_endtime
            owner1 = assignedtable[0].owner
            if start1>current_time and ((start1-current_time).seconds)<=300:
                content = "Dear"+ owner1 +":<br><br>你申请的zebu资源即将可以开始使用<br>开始使用时间："+str(start1+datetime.timedelta(hours=8))
                subject = resource+'资源即将可以使用'
                # use sendEmailTest.send_mail() at Nanjing thundersoft site, use sendEmail.send_mail() at spreadtrum site
                if "@spreadst.com" in owner1:
                    receivers = [owner1]
                    result = sendEmailTest.send_mail(subject, content, receivers)
                else:
                    receivers = [owner1 + '@spreadtrum.com', 'nicole.wang@spreadtrum.com', 'chunsi.he@spreadtrum.com',
                                 'chunji.chen@spreadtrum.com', 'fiona.zhang@spreadtrum.com',
                                 'xinpeng.li@spreadtrum.com', 'guoliang.ren@spreadtrum.com',
                                 'ellen.yang@spreadtrum.com']
                    result = sendEmail.send_mail(subject, content, receivers)
                if result:
                    print "send success"
                else:
                    print"send fail"
            elif start1<current_time and ((end1-current_time).seconds)<=300:
                content = "Dear" + owner1 + ":<br><br>你申请的zebu资源即将被释放<br>释放时间："+str(end1+datetime.timedelta(hours=8))
                subject = resource+'资源即将被释放'
                # use sendEmailTest.send_mail() at Nanjing thundersoft site, use sendEmail.send_mail() at spreadtrum site
                if "@spreadst.com" in owner1:
                    receivers = [owner1]
                    result = sendEmailTest.send_mail(subject, content, receivers)
                else:
                    receivers = [owner1 + '@spreadtrum.com', 'nicole.wang@spreadtrum.com', 'chunsi.he@spreadtrum.com',
                                 'chunji.chen@spreadtrum.com', 'fiona.zhang@spreadtrum.com',
                                 'xinpeng.li@spreadtrum.com', 'guoliang.ren@spreadtrum.com',
                                 'ellen.yang@spreadtrum.com']
                    result = sendEmail.send_mail(subject, content, receivers)
                if result:
                    print "send success"
                else:
                    print"send fail"
                if len(assignedtable)>1:
                    start2 = assignedtable[1].assign_starttime
                    owner2 = assignedtable[1].owner
                    if ((start2-current_time).seconds)<=300:
                        content = "Dear" + owner2 + "::<br><br>你申请的zebu资源即将可以开始使用<br>开始使用时间："+str(start2+datetime.timedelta(hours=8))
                        subject = resource+'资源即将开始使用'
                        # use sendEmailTest.send_mail() at Nanjing thundersoft site, use sendEmail.send_mail() at spreadtrum site
                        if "@spreadst.com" in owner2:
                            receivers = [owner2]
                            result = sendEmailTest.send_mail(subject, content, receivers)
                        else:
                            receivers = [owner2 + '@spreadtrum.com', 'nicole.wang@spreadtrum.com',
                                         'chunsi.he@spreadtrum.com',
                                         'chunji.chen@spreadtrum.com', 'fiona.zhang@spreadtrum.com',
                                         'xinpeng.li@spreadtrum.com', 'guoliang.ren@spreadtrum.com',
                                         'ellen.yang@spreadtrum.com']
                            result = sendEmail.send_mail(subject, content, receivers)
                        if result:
                            print "send success"
                        else:
                            print"send fail"
    # print current_time


if __name__ == "__main__":
    main()
    print('Done!')