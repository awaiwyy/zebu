#!/usr/bin/env python
#coding:utf-8

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zebu.settings")

'''
Django 版本大于等于1.7的时候，需要加上下面两句
import django
django.setup()
否则会抛出错误 django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
'''

import django
if django.VERSION >= (1, 7):#自动判断版本
    django.setup()

import datetime
from datetime import timedelta
from dateutil.tz import *
def main():
    from apps.request.models import RequestTable
    
    current = datetime.datetime.now(tzutc())

    oldtime1 = current + datetime.timedelta(days=-2)
    oldtime2 = current + datetime.timedelta(days=-1)
    newtime1 = current + datetime.timedelta(days=1)
    newtime2 = current + datetime.timedelta(days=3)
    newtime3 = current + datetime.timedelta(days=5)
    newtime4 = current + datetime.timedelta(days=7)
    record=[]
    #CN_ZEBU_M0 assign_starttime在未来newtime1
    item0=["iwhale2","Performance","APPS","Power-CHIP","GFS Benchmark","Zebu-JC","15Hour02Day01Piece","gaijy0309@spreadst.com","Normal","2016-09-07","ongoing","true","Yes",oldtime1,"CN_ZEBU_M0","CN_ZEBU_M0",newtime1,newtime2]
    #CN_ZEBU_M1 没有assign，申请时间oldtime1
    item1=["iwhale2","Performance","APPS","Power-CHIP","GFS Benchmark","Zebu-JC","15Hour02Day01Piece","gaijy0309@spreadst.com","Normal","2016-09-07","ongoing","false","No",oldtime1,"CN_ZEBU_M1","",None,None]
    #CN_ZEBU_M1 没有assign，newtime1
    item2=["iwhale2","Performance","APPS","Power-CHIP","GFS Benchmark","Zebu-JC","15Hour02Day01Piece","gaijy0309@spreadst.com","Normal","2016-09-07","ongoing","true","Yes",newtime1,"CN_ZEBU_M1","",None,None]
    #CN_ZEBU_M1 assign_endtime在过去，不应列在队列中
    item3=["iwhale2","Performance","APPS","Power-CHIP","GFS Benchmark","Zebu-JC","15Hour02Day01Piece","gaijy0309@spreadst.com","Normal","2016-09-07","ongoing","true","Yes",oldtime1,"CN_ZEBU_M1","CN_ZEBU_M1",oldtime1,oldtime2]
    #CN_ZEBU_M1 currenttime在assign_starttime和assign_endtime之间
    item4=["iwhale2","Performance","APPS","Power-CHIP","GFS Benchmark","Zebu-JC","15Hour02Day01Piece","gaijy0309@spreadst.com","Normal","2016-09-07","ongoing","true","Yes",oldtime1,"CN_ZEBU_M1","CN_ZEBU_M1",oldtime1,newtime1]
    # CN_ZEBU_M1 assign_starttime等于上一条的assign_endtime，totalleft 应该算上该时间
    item5=["iwhale2","Performance","APPS","Power-CHIP","GFS Benchmark","Zebu-JC","15Hour02Day01Piece","gaijy0309@spreadst.com","Normal","2016-09-07","ongoing","true","Yes",oldtime1,"CN_ZEBU_M1,CN_ZEBU_M2","CN_ZEBU_M1,CN_ZEBU_M2",newtime1,newtime2]
    # CN_ZEBU_M1 assign_starttime不等于上一条的assign_endtime，totalleft 不会算上该时间
    item6=["iwhale2","Performance","APPS","Power-CHIP","GFS Benchmark","Zebu-JC","15Hour02Day01Piece","gaijy0309@spreadst.com","Normal","2016-09-07","ongoing","true","Yes",oldtime1,"CN_ZEBU_M1","CN_ZEBU_M1",newtime3,newtime4]
    #CN_ZEBU_M2 没有assign
    item7=["iwhale2","Performance","APPS","Power-CHIP","GFS Benchmark","Zebu-JC","15Hour02Day01Piece","gaijy0309@spreadst.com","Normal","2016-09-07","ongoing","true","Yes",oldtime2,"CN_ZEBU_M2","",None,None]
    record.append(item0)
    record.append(item1)
    record.append(item2)
    record.append(item3)
    record.append(item4)
    record.append(item5)
    record.append(item6)
    record.append(item7)
    # print record


    for item in record:
        RequestTable.objects.get_or_create(
                                project = item[0],
                                classification=item[1],
                                module = item[2],
                                tf_case=item[3],
                                action_discription = item[4],
                                environment = item[5],
                                request_duration = item[6],
                                owner = item[7],
                                priority = item[8],
                                submit_date = item[9],
                                status = item[10],
                                is_plan = item[11],
                                acceptance = item[12],
                                application_time =item[13],
                                server_ID = item[14],
                                assign_ID = item[15],
                                assign_starttime = item[16],
                                assign_endtime = item[17]
                                )


if __name__ == "__main__":
    main()
    print('Done!')