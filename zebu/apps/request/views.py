#coding:utf-8
from __future__ import division
from django.http import HttpResponse
from django.http import HttpResponseRedirect,StreamingHttpResponse
from django.shortcuts import render
from ..request.models import RequestTable
from ..newhome.models import ResourceTable
from common import com_def
from ..request.models import TotalTable
import os
import math
import time, datetime
import json
import thread
import sys
from common import xlwt
from common import sendEmail
from email.mime.text import MIMEText
from email.header import Header
import copy


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from models import RequestTable
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Create your views here.
temp_dir = os.path.join(BASE_DIR, "resources/tab/")
# Create your views here.
# temp_dir = "resources/tab/"
request_file = "request_tab.xls"

def saveRequestTab(request_tab,file_name):
    #set style
    font0 = xlwt.Font()
    font0.bold = True
    style0 = xlwt.XFStyle()
    style0.font = font0

    style = xlwt.XFStyle()
    style.num_format_str = 'YYYY-MM-DD'

    style1 = xlwt.XFStyle()
    style1.num_format_str = 'YYYY-MM-DD h:mm'
    #creat sheet
    wb = xlwt.Workbook(encoding = 'utf-8')
    sheet = wb.add_sheet(u'request_tab', cell_overwrite_ok=True)

    row = 0  
    sheet.write(row, 0, 'ID', style0)
    sheet.write(row, 1, 'Product', style0)
    sheet.write(row, 2, 'TF Case', style0)
    sheet.write(row, 3, 'Classification', style0)
    sheet.write(row, 4, 'Module', style0)
    sheet.write(row, 5, 'Action Description', style0)
    sheet.write(row, 6, 'Environment', style0)
    sheet.write(row, 7, 'Request Duration', style0)
    sheet.write(row, 8, 'Owner', style0)
    sheet.write(row, 9, 'Priority', style0)
    sheet.write(row, 10, 'Server ID', style0)
    sheet.write(row, 11, 'Application Time', style0)
    sheet.write(row, 12, 'Submit Date', style0)
    sheet.write(row, 13, 'Acceptance', style0)

    row += 1
    
    for tab in request_tab:
        sheet.write(row, 0, tab.id)
        sheet.write(row, 1, tab.project)
        sheet.write(row, 2, tab.tf_case)
        sheet.write(row, 3, tab.classification)
        sheet.write(row, 4, tab.module)
        sheet.write(row, 5, tab.action_discription)
        sheet.write(row, 6, tab.environment)
        sheet.write(row, 7, tab.request_duration)
        sheet.write(row, 8, tab.owner)
        sheet.write(row, 9, tab.priority)
        sheet.write(row, 10, tab.server_ID)
        if tab.application_time:
            sheet.write(row, 11, (tab.application_time+ datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M"))
        sheet.write(row, 12, tab.submit_date, style)
        sheet.write(row, 13, tab.acceptance)
        row += 1
    wb.save(file_name)

def file_iterator(file_name, chunk_size=512):
    with open(file_name,"rb") as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

def exportRequestTab(request):
    request_tab = RequestTable.objects.all().order_by("-id")
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
    #file_name = temp_dir + request_file
    today = time.strftime("%Y_%m_%d", time.localtime())
    file_name = today + "_" + request_file
    saveRequestTab(request_tab,file_name)

    response = StreamingHttpResponse(file_iterator(file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)

    return response

def requestUser(request, **kwargs):
    resource_tab = ResourceTable.objects.all().order_by("id")
    resourceid_list=[]
    for tab in resource_tab:
        resourceid_list.append(tab.resource_id)
    acceptancelist=com_def.acceptancelist[:]
    gopage = request.GET.get('page')
    if (gopage == None):
        gopage = "1"
    #show request table
    request_tab = RequestTable.objects.all().order_by("-id")
    #for request duration
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
    #deal with application
    if request.method == 'POST':
        #获得表单数据
        if 'projectInfo' in request.POST.keys():
            print"into new request tab"
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
            if request.POST['durationHourEdit'] and request.POST['durationDayEdit'] and request.POST[
                'durationPieceEdit']:
                request_duration = request.POST['durationHourEdit'] + "Hour" + request.POST['durationDayEdit'] + "Day" + \
                                   request.POST['durationPieceEdit'] + "Piece"
                daily_duration=str(0)+"Hour"+request.POST['durationPieceEdit'] + "Piece"
            #添加到数据库
                #print [project, tf_case, classification, module, action_discription,
                   #environment, request_duration, owner, priority]
                RequestTable.objects.create(project = project,
                                tf_case = tf_case,
                                classification = classification,
                                module = module,
                                action_discription = action_discription,
                                environment = environment,
                                request_duration = request_duration,
                                daily_duration=daily_duration,
                                owner = owner,
                                priority = priority,
                                server_ID = server_ID,
                                application_time =application_time)

                #receivers = [owner+'@spreadtrum.com','nicole.wang@spreadtrum.com','chunsi.he@spreadtrum.com','chunji.chen@spreadtrum.com','fiona.zhang@spreadtrum.com','xinpeng.li@spreadtrum.com','guoliang.ren@spreadtrum.com']
                receivers = [owner+'@spreadtrum.com']
                #TF case/申请人/申请使用开始时间/daily duration/申请使用的zebu
                content = "Dear Managers:<br><br>新增一个zebu资源申请，请知悉并及时处理，申请信息如下，<br>申请人："+owner+"<br>Description："+action_discription+"<br>TF case："+tf_case+"<br>Request_duration:"+request_duration+"<br>Application Time:"+application_time+"<br>Request Zebu Resource ID:"+server_ID+"<br><br>管理系统地址：<a href='http://10.5.2.62'>http://10.5.2.62;</a><br>登录方式为外网域帐号。"
                subject = owner+'创建了一个zebu资源申请，请登录指定服务器处理'
                
                if sendEmail.send_mail(subject,content,receivers):
                    print "send success"
                else:
                    print"send fail"
                
        elif 'delRqId' in request.POST.keys():
            #print "into delete request tab"
            del_id = request.POST['delRqId']
            del_request = RequestTable.objects.get(id = del_id)
            del_request.delete()
        #else:
            #print "there is something wrong"
        #update request table
        #request_tab = RequestTable.objects.all().order_by("-submit_date")

        for tab in request_tab:
            tab.action_discription = tab.action_discription.replace("\n", "<br>")
        return HttpResponseRedirect('/request/', {"request_tab": request_tab, 'valid_duration': valid_duration,"productlist":productlist,"resourceid_list":resourceid_list}) #avoid submit twice when entering"F5"
    else:
        serverid_list={}
        for tab in request_tab:
            tab.action_discription = tab.action_discription.replace("\n", "<br>")
            serverid=tab.server_ID.split(",")
            serverid_unselected=copy.deepcopy(resourceid_list)
            if serverid != ['']:
                for id in serverid:
                    serverid_unselected.remove(id)
            serverid_list[tab.id]=[serverid,serverid_unselected]
        filter = ""
        prodtlist = productlist
        acceptlist = acceptancelist
        order = "-id"
        otherpara = ""
        if "p" in request.GET.keys():
            if  request.GET.get("p") != "":
                prodtlist = []
                filter_product = request.GET.get("p")[1:].split(",p")
                for item in filter_product:
                    prodtlist.append(productlist[int(item)-1])
                    filter += "p" + item + ","
            otherpara += "&p=" + request.GET.get("p")
        if "a" in request.GET.keys():
            if  request.GET.get("a") != "":
                acceptlist = []
                filter_acceptance = request.GET.get("a")[1:].split(",a")
                for item in filter_acceptance:
                    acceptlist.append(acceptancelist[int(item)-1])
                    filter += "a" + item + ","
            otherpara += "&a=" + request.GET.get("a")
        if "order" in request.GET.keys():
            if request.GET.get("order") == "up":
                order = "project"
            if request.GET.get("order") == "down":
                order = "-project"
            otherpara += "&order=" + request.GET.get("order")

        request_tab = RequestTable.objects.filter(project__in=prodtlist, acceptance__in=acceptlist).order_by(order)

        perpage = 15 #show how many items per page
    
        objects = request_tab
        pager = Paginator(objects,perpage)
        num_pages = pager.num_pages
        try:
            projects = pager.page(gopage)

        except PageNotAnInteger:
            projects = pager.page(1)
        except EmptyPage:
            projects = pager.page(pager.num_pages)
        
        # Pagination range
        # pages_left: how many page numbers show on left of current page at most
        # pages_right: how many page numbers show on right of current page at most
        pages_left = 4
        pages_right = 4
        current_page = gopage
        range_left = "norange"
        range_right = "norange"
        over_range_left = "false"
        over_range_right = "false"

        #Range Left
        if (int(gopage)-1 > pages_left):
            over_range_left = "true"
            range_left = range(int(gopage) - pages_left, int(gopage))
        if (int(gopage)-1 == pages_left):
            range_left = range(1, int(gopage))
        if (int(gopage)-1 < pages_left):
            range_left = range(1, int(gopage))
        
        #Range Right
        if (int(gopage) < pager.num_pages - pages_right):
            over_range_right = "true"
            range_right = range(int(gopage) + 1, int(gopage) + 1 + pages_right)
        if (int(gopage) == pager.num_pages - pages_right):
            range_right = range(int(gopage) + 1, int(gopage) + 1 + pages_right)
        if (int(gopage) > pager.num_pages - pages_right):
            range_right = range(int(gopage) + 1, pager.num_pages + 1)
        
        return render(request, 'request/request.html', {
            "request_tab": projects, 
            'valid_duration': valid_duration, 
            'range_left': range_left, 
            'range_right': range_right, 
            'over_range_left': over_range_left, 
            'over_range_right': over_range_right,
            "productlist": productlist,
            "acceptancelist":acceptancelist,
            "filter": filter,
            "order": order,
            "otherpara": otherpara,
            "resourceid_list":resourceid_list,
            "serverid_list":serverid_list})

def ajaxpost(request):
    edit_id = request.POST['idEdit']
    edit_request = RequestTable.objects.get(id=edit_id)
    edit_request.project = request.POST['projectEdit']
    edit_request.tf_case = request.POST['tfcaseEdit']
    edit_request.classification = request.POST['classificationEdit']
    edit_request.module = request.POST['moduleEdit']
    edit_request.action_discription = request.POST['actionDiscriptionEdit']
    edit_request.environment = request.POST['environmentEdit']
    request_duration = request.POST['durationHourEdit']+"Hour"+request.POST['durationDayEdit']+"Day"+request.POST['durationPieceEdit']+"Piece"
    edit_request.request_duration = request_duration
    edit_request.priority = request.POST['priorityEdit']
    server_ID=""
    for i in request.POST.getlist('serverIdEdit[]'):
        if i != "":
            server_ID += i + ","
    edit_request.server_ID = server_ID[:-1] 
    if request.POST['applicationTimeEdit'] != '':
        edit_request.application_time = request.POST['applicationTimeEdit']
    edit_request.save()
    success_dict = {'request_duration': request_duration}
    return HttpResponse(json.dumps(success_dict),
                        content_type="application/json")
