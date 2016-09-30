#coding:utf-8
from __future__ import division
from django.shortcuts import render
from django.http import HttpResponseRedirect,StreamingHttpResponse
from common import com_def
import datetime
from dateutil.tz import *

from ..request.models import RequestTable
from models import ResourceTable
from common import sendEmail
from common import sendEmailTest

# Create your views here.

def getHomeData(resourcetable): 
    resource_list = []
    n = 0
    for tab in resourcetable:
        j = 0
        task_item = []
        resource_row = {}
        n = n + 1
        resource = tab.resource_id
        status = "Free"
        current_left = ''
        total_left = ''
        user = ''
        # 获取当前时间（+0:00时区）
        current_time = datetime.datetime.now(tzutc())
        assignedtable = RequestTable.objects.filter(assign_ID__contains=resource, assign_starttime__isnull=False,assign_endtime__gt=current_time).order_by("assign_starttime")
        requesttable = RequestTable.objects.filter(server_ID__contains=resource,application_time__isnull=False,assign_starttime__isnull=True).order_by("application_time")
        assign_num = RequestTable.objects.filter(assign_ID__contains=resource, assign_starttime__isnull=False,assign_endtime__gt=current_time).count()
        request_num = RequestTable.objects.filter(server_ID__contains=resource,application_time__isnull=False, assign_starttime__isnull=True).count()
        if assignedtable:
            assigned_starttime = assignedtable[0].assign_starttime  # 队列第一个任务的assign_starttime
            assigned_endtime = assignedtable[0].assign_endtime  # 队列第一个任务的assign_endtime
            if assigned_starttime < current_time:
                status = "Busy"
                user = assignedtable[0].owner
                current_delta = assigned_endtime - current_time  # 相差的时间
                current_left = current_delta.days * 24 + round(current_delta.seconds / 3600, 1)  # 换成小时为单位,小数点后一位
                total_endtime = assigned_endtime  # total_left的结束时间
                for i in range(assign_num - 1):
                    if assignedtable[i].assign_endtime == assignedtable[i + 1].assign_starttime:
                        total_endtime = assignedtable[i + 1].assign_endtime
                    else:
                        break
                total_delta = total_endtime - current_time
                total_left = total_delta.days * 24 + round(total_delta.seconds / 3600, 1)  # 换成小时为单位
            for item in assignedtable:
                j = j + 1
                task_row = {}
                # print "j=" ,j
                product = item.project
                description = item.action_discription
                priority = item.priority
                ass_starttime = item.assign_starttime
                ass_endtime = item.assign_endtime
                req_starttime = item.application_time
                delta_days = int((item.request_duration.split('r')[1]).split('D')[0])
                if req_starttime:
                    req_endtime = req_starttime + datetime.timedelta(days=delta_days)
                else:
                    req_endtime = None
                item_status = "Wait"
                if ass_starttime < current_time:
                    item_status = "Inprogress"
                item_user = item.owner
                task_row['Num'] = j
                task_row['product'] = product
                task_row['description'] = description
                task_row['priority'] = priority
                task_row['ass_starttime'] = ass_starttime
                task_row['ass_endtime'] = ass_endtime
                task_row['req_starttime'] = req_starttime
                task_row['req_endtime'] = req_endtime
                task_row['item_status'] = item_status
                task_row['item_user'] = item_user
                task_item.append(task_row)
                # print "num",task_row['Num']
                # print "itemqqq",task_item
        if requesttable:
            for item in requesttable:
                j = j + 1
                task_row = {}
                # print "rr j=", j
                product = item.project
                description = item.action_discription
                priority = item.priority
                ass_starttime = item.assign_starttime
                ass_endtime = item.assign_endtime
                req_starttime = item.application_time
                delta_days = int((item.request_duration.split('r')[1]).split('D')[0])
                req_endtime = req_starttime + datetime.timedelta(days=delta_days)
                item_status = "Wait"
                item_user = item.owner
                task_row['Num'] = j
                task_row['product'] = product
                task_row['description'] = description
                task_row['priority'] = priority
                task_row['ass_starttime'] = ass_starttime
                task_row['ass_endtime'] = ass_endtime
                task_row['req_starttime'] = req_starttime
                task_row['req_endtime'] = req_endtime
                task_row['item_status'] = item_status
                task_row['item_user'] = item_user
                task_item.append(task_row)
                # print "num", task_row['Num']
        task_num = assign_num + request_num
        if task_num==0:
            task_num=''
        # print number , resource, status , current_left, total_left, task_num
        resource_row['number'] = n
        resource_row['resource'] = resource
        resource_row['status'] = status
        resource_row['current_left'] = current_left
        resource_row['total_left'] = total_left
        resource_row['user'] = user
        resource_row['task_num'] = task_num
        resource_row['task_item'] = task_item
        # print "qqqqqqqqqq",resource_row['task_item']
        resource_list.append(resource_row)
    return resource_list

def newHomePage(request, **kwargs):
    resource_tab = ResourceTable.objects.all().order_by("id")
    resourceid_list = []
    for tab in resource_tab:
        resourceid_list.append(tab.resource_id)
    resourcetable = ResourceTable.objects.all()
    resource_list = getHomeData(resourcetable)
    valid_duration = []
    valid_requestduration_piece = []
    valid_requestduration_day = []
    valid_requestduration_hour = []
    for day in range(1, 32):
        if day < 10:
            day = "0" + str(day)
        valid_requestduration_day.append(day)
    for hour in range(0, 25):
        if hour < 10:
            hour = "0" + str(hour)
        valid_requestduration_hour.append(hour)
    for i in range(1, 11):
        if i < 10:
            piece = "0" + str(i)
        else:
            piece = i
        valid_requestduration_piece.append(piece)
    valid_duration.append(valid_requestduration_hour)
    valid_duration.append(valid_requestduration_day)
    valid_duration.append(valid_requestduration_piece)
    productlist = com_def.productlist[:]
    city_list = com_def.city_list[:]
    environment_list = com_def.environment_list[:]
    if request.method == 'POST':
        if 'projectInfo' in request.POST.keys():
            print "into new request from home"
            project = request.POST['projectInfo']
            tf_case = request.POST['tfcaseInfo']
            classification = request.POST['classificationInfo']
            module = request.POST['moduleInfo']
            action_discription = request.POST['actionDiscriptionInfo']
            environment = request.POST['environmentInfo']
            owner = request.POST['ownerInfo']
            priority = request.POST['priorityInfo']
            server_ID=""
            for i in request.POST.getlist('serverId'):
                server_ID += i + ","
            server_ID = server_ID[:-1]
            application_time = request.POST['applicationTime']
            if request.POST['durationHourEdit'] and request.POST['durationDayEdit'] and request.POST['durationPieceEdit']:
                request_duration = request.POST['durationHourEdit'] + "Hour" + request.POST['durationDayEdit'] + "Day" + \
                                   request.POST['durationPieceEdit'] + "Piece"
                daily_duration = str(0) + "Hour" + request.POST['durationPieceEdit'] + "Piece"
                # 添加到数据库
                RequestTable.objects.create(project=project,
                                            tf_case=tf_case,
                                            classification=classification,
                                            module=module,
                                            action_discription=action_discription,
                                            environment=environment,
                                            request_duration=request_duration,
                                            daily_duration=daily_duration,
                                            owner=owner,
                                            priority=priority,
                                            server_ID=server_ID,
                                            application_time=application_time)


                # TF case/申请人/申请使用开始时间/daily duration/申请使用的zebu
                content = "Dear Managers:<br><br>新增一个zebu资源申请，请知悉并及时处理，申请信息如下，<br>申请人：" + owner + "<br>Description：" + action_discription + "<br>TF case：" + tf_case + "<br>Request_duration:" + request_duration + "<br>Application Time:" + application_time + "<br>Request Zebu Resource ID:" + server_ID + "<br><br>管理系统地址：<a href='http://10.5.2.62'>http://10.5.2.62;</a><br>登录方式为外网域帐号。"
                subject = owner + '创建了一个zebu资源申请，请登录指定服务器处理'
                # use sendEmailTest.send_mail() at Nanjing thundersoft site, use sendEmail.send_mail() at spreadtrum site
                if "@spreadst.com" in owner:
                    receivers = [owner]
                    result = sendEmailTest.send_mail(subject, content, receivers)
                else:
                    receivers = [owner+'@spreadtrum.com','nicole.wang@spreadtrum.com','chunsi.he@spreadtrum.com','chunji.chen@spreadtrum.com','fiona.zhang@spreadtrum.com','xinpeng.li@spreadtrum.com','guoliang.ren@spreadtrum.com','ellen.yang@spreadtrum.com']
                    result = sendEmail.send_mail(subject, content, receivers)
                if result:
                    print "send success"
                else:
                    print"send fail"

        return HttpResponseRedirect('/home/', {'valid_duration': valid_duration, "city_list": city_list,"environment_list":environment_list,"productlist":productlist,"resourceid_list":resourceid_list,"resource_list":resource_list})
    else:
        filter = ""
        citylist = city_list
        environmentlist = environment_list
        if "c" in request.GET.keys():
            if  request.GET.get("c") != "":
                citylist = []
                filter_city = request.GET.get("c")[1:].split(",c")
                for item in filter_city:
                    citylist.append(city_list[int(item)-1])
                    filter += "c" + item + ","
        if "e" in request.GET.keys():
            if  request.GET.get("e") != "":
                environmentlist = []
                filter_environment = request.GET.get("e")[1:].split(",e")
                for item in filter_environment:
                    environmentlist.append(environment_list[int(item)-1])
                    filter += "e" + item + ","
        resourcetable = ResourceTable.objects.filter(city__in=citylist,environment__in=environmentlist)
        resource_list = getHomeData(resourcetable)
        return render(request, 'newhome/newhome.html', {'valid_duration': valid_duration, "city_list": city_list,"environment_list":environment_list,"productlist":productlist,"filter":filter,"resourceid_list":resourceid_list,"resource_list":resource_list})


