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


def main():

    from apps.request.models import RequestTable
    from apps.request.models import TotalTable
    import datetime

    plan_tab = RequestTable.objects.filter(is_plan="true").order_by("-id")

    for tab in plan_tab:
        stime = tab.start_time
        if stime:
            stime = stime + datetime.timedelta(hours=8)
            ftimestr = stime.strftime('%Y-%m-%d %H:%M:%S')
            # print "ftimestr=",ftimestr
            ftime1 = ftimestr.split(' ')[0]
            ftime = datetime.datetime.strptime(ftime1, '%Y-%m-%d').date()
            # ftime = datetime.datetime.strptime(stime.strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S').date()
            # print "ftime=",ftime
            cur_time = datetime.date.today()
            # ctime = datetime.datetime.utcnow()
            # stime = datetime.datetime.strptime(stime.strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
            total = 0
            if "close" != tab.status:
                if cur_time >= ftime:
                    total_tab1 = TotalTable.objects.filter(request_id=tab.id).order_by("-change_date")
                    if total_tab1:
                        recent_edit = total_tab1[0]
                        rtime = recent_edit.change_date
                        delta = (cur_time - rtime).days
                        # print "delta=",delta
                        # print "len(total_tab1)",len(total_tab1)
                        for i in range(delta):
                            # Totaltable中最大日期到今天相差天数的数据，按照前一天的数据补入：
                            # 1.若前一天状态为ongoing，当天的daily_duration值和前一天一样；
                            # 2.若前一天状态不是ongoing，当天的daily_duration值Hour为0，pieces为前一天daily_duration的pieces；
                            itime = rtime + datetime.timedelta(days=i + 1)
                            # print itime
                            try:
                                lastday = total_tab1.get(change_date=(itime - datetime.timedelta(days=1)))
                                daily_hour = tab.daily_duration.split('H')[0]
                                daily_piece = tab.daily_duration.split('r')[1]
                                if lastday.status == 'ongoing':
                                    TotalTable.objects.get_or_create(change_date=itime,
                                                                        daily_duration=daily_hour + "Hour" + daily_piece,
                                                                        status=lastday.status,
                                                                        request_id=lastday.request_id)
                                else:
                                    TotalTable.objects.get_or_create(change_date=itime,
                                                                        daily_duration='00Hour' + daily_piece,
                                                                        status=lastday.status,
                                                                        request_id=lastday.request_id)
                            except:
                                pass
                    else:
                        request_piece = tab.request_duration.split('y')[1]
                        delta = (cur_time - ftime).days
                        for i in range(delta):
                            itime = ftime + datetime.timedelta(days=i)
                            TotalTable.objects.create(change_date=itime,
                                                        daily_duration='00Hour' + request_piece,
                                                        status="ongoing",
                                                        request_id=tab.id)
                        daily_hour = tab.daily_duration.split('H')[0]
                        daily_piece = tab.daily_duration.split('r')[1]
                        TotalTable.objects.create(change_date=cur_time,
                                                    daily_duration=daily_hour + "Hour" + daily_piece,
                                                    status=tab.status,
                                                    request_id=tab.id)
                    i = 0
                    totaldelta = (cur_time - ftime).days
                    for i in range(totaldelta + 1):
                        itime = ftime + datetime.timedelta(days=i)
                        try:
                            curday = total_tab1.get(change_date=itime)
                            if curday.status == 'ongoing':
                                idaily_h = int(curday.daily_duration.split('H')[0])
                                idaily_p = int((curday.daily_duration.split('r')[1]).split('P')[0])
                                total = total + idaily_h * idaily_p
                        except:
                            pass
            else:
                total_tab1 = TotalTable.objects.filter(request_id=tab.id).order_by("-change_date")
                ctime = tab.close_time
                ctime = ctime + datetime.timedelta(hours=8)
                ctimestr = ctime.strftime('%Y-%m-%d %H:%M:%S')
                ctime1 = ctimestr.split(' ')[0]
                ctime = datetime.datetime.strptime(ctime1, '%Y-%m-%d').date()
                totaldelta1 = (ctime - ftime).days
                i = 0
                for i in range(totaldelta1 + 1):
                    # 计算total的值
                    itime = ftime + datetime.timedelta(days=i)
                    try:
                        curday = total_tab1.get(change_date=itime)
                        if curday.status == 'ongoing':
                            idaily_h = int(curday.daily_duration.split('H')[0])
                            idaily_p = int((curday.daily_duration.split('r')[1]).split('P')[0])
                            total = total + idaily_h * idaily_p
                    except:
                        pass
            tab.duration = total
            # 判断total值是否超过request的值
            request_h = int(tab.request_duration.split('H')[0])
            request_d = int((tab.request_duration.split('r')[1]).split('D')[0])
            request_p = int((tab.request_duration.split('y')[1]).split('P')[0])
            request_hours = request_h * request_d * request_p
            # print "request_hours" , request_hours
            if total >= request_hours:
                tab.isdelay = 'delay'
            elif 'delay' == tab.isdelay:
                tab.isdelay = 'no'  
            tab.save()

if __name__ == "__main__":
    main()
    print('Done!')