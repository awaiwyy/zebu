#coding:utf-8
from django.http import HttpResponseRedirect,StreamingHttpResponse
from django.shortcuts import render
from models import ReportTable
from ..request.models import RequestTable
from models import ResourceUsageTable
from models import ResourceUsageTitleTable
from models import MaintfstatusTable
from models import ScheduleTable
import os
from PIL import Image
import sys

# Create your views here.
upload_dir = "resources/upload/"
def reportPage(request):
    daily_report_tab = ReportTable.objects.filter(is_daily_report="true").order_by("id")
    #daily_report_tab = ReportTable.objects.all()
    if request.method == 'POST':
        print "POST!!!!"
        #print request.body
        # 获得表单数据
        if 'productInfo' in request.POST.keys():
            print"into new daily report "
            handle_uploaded_file(request.FILES['file'], str(request.FILES['file']))
            product = request.POST['productInfo']
            spm = request.POST['spmInfo']
            reporter = request.POST['reporterInfo']
            file_link=str(request.FILES['file'])
            # 添加到数据库
            ReportTable.objects.create(product=product,
                                       spm=spm,
                                       daily_reporter=reporter,
                                       file_link =file_link,
                                       )
        elif "idEdit" in request.POST.keys():
            print "into new report table"
            edit_id = request.POST['idEdit']
            edit_report = ReportTable.objects.get(id=edit_id)
            edit_report.product = request.POST['productEdit']
            edit_report.spm = request.POST['spmEdit']
            edit_report.daily_reporter = request.POST['reporterEdit']
            if 'file_linkEdit' in request.FILES:
                handle_uploaded_file(request.FILES['file_linkEdit'], str(request.FILES['file_linkEdit']))
                edit_report.file_link = str(request.FILES['file_linkEdit'])
            edit_report.save()
        elif 'delReportId' in request.POST.keys():
            print "into delete plan"
            del_id = request.POST['delReportId']
            del_report = ReportTable.objects.get(id=del_id)
            del_report.is_daily_report = 'false'
            del_report.save()
        else:
            print "there is something wrong"
        return HttpResponseRedirect('/report/', {"daily_report_tab": daily_report_tab})
    else:
        print "GET!!!!"
        return render(request, 'report/report.html', {"daily_report_tab": daily_report_tab})
        #   return render(request, 'report/report.html')

def handle_uploaded_file(file, filename):
    if not os.path.exists(upload_dir):
        os.mkdir(upload_dir)
    with open(upload_dir + filename.decode('utf-8'), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    pic_list=["jpg","png","gif","bmp","jpeg"]
    if filename.split(".")[-1] in pic_list:
        img = Image.open(upload_dir + filename.decode('utf-8'))
        img.thumbnail((100, 100), Image.ANTIALIAS)
        img.save(upload_dir + "mini" +filename.decode('utf-8'))

def file_iterator(filename, chunk_size=512):
    with open(filename,"rb") as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

def file_Download(request,filename):
        file_name = upload_dir+ filename
        response = StreamingHttpResponse(file_iterator(file_name))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)
        return response

def report_Resource(request):
    title_tab = ResourceUsageTitleTable.objects.all()
    resource_usage_tab = ResourceUsageTable.objects.filter(is_show="true").order_by("id")
    if request.method == 'POST':
        print "POST!!!!"
        # 获得表单数据
        if 'productInfo' in request.POST.keys():
            print"into new resource uasge"
            product = request.POST['productInfo']
            spm = request.POST['spmInfo']
            reporter = request.POST['reporterInfo']
            # 添加到数据库
            ResourceUsageTable.objects.create(product=product,
                                             spm=spm,
                                             daily_reporter=reporter,
                                             total=0,
                                              power_management=0,
                                              performance=0,
                                              function=0,
                                              zebu_platform=0)
        elif 'edittotal0' in request.POST.keys():
            print "edit total and usage"
            edit_id = request.POST["idEdit110"]
            print edit_id
            total = request.POST["edittotal0"]
            usage = request.POST["editusage0"]
            ResourceUsageTitleTable.objects.create(usage=usage,
                                                   total=total)
        elif 'edittotal' in request.POST.keys():
            print "edit total and usage"
            edit_id =request.POST["idEdit11" ]
            print edit_id
            total = request.POST["edittotal"]
            usage = request.POST["editusage"]
            edittitle_tab = ResourceUsageTitleTable.objects.get(id=edit_id)
            edittitle_tab.total= total
            edittitle_tab.usage = usage
            edittitle_tab.save()
        elif 'productEdit' in request.POST.keys():
            print"edit resource uasge"
            edit_id = request.POST['idEdit']
            edit_resource = ResourceUsageTable.objects.get(id=edit_id)
            edit_resource.product = request.POST['productEdit']
            edit_resource.spm = request.POST['spmEdit']
            edit_resource.daily_reporter = request.POST['reporterEdit']
            edit_resource.total = request.POST['totalEdit']
            edit_resource.power_management = request.POST['managementEdit']
            edit_resource.performance = request.POST['performanceEdit']
            edit_resource.function = request.POST['functionEdit']
            edit_resource.zebu_platform = request.POST['zubeEdit']
            print edit_resource.total
            edit_resource.save()
        elif 'delresourceId' in request.POST.keys():
            print "into delete resource"
            del_id = request.POST['delresourceId']
            del_resource = ResourceUsageTable.objects.get(id=del_id)
            del_resource.is_show = 'false'
            del_resource.save()
        else:
            print "there is something wrong"
        return HttpResponseRedirect('resource_usage', {"resource_usage_tab": resource_usage_tab,"title_tab": title_tab})
    else:
        print "GET!!!!"
        return render(request, 'report/resource_usage.html',{"resource_usage_tab": resource_usage_tab,"title_tab": title_tab})

def report_MainTF(request):
    plan_tab = RequestTable.objects.filter(is_plan="true",is_maintf="false")
    is_maintf_tab=RequestTable.objects.filter(is_plan="true",is_maintf="true")
    is_high_tab=is_maintf_tab.filter(is_high="true")
    is_low_tab = is_maintf_tab.filter(is_low="true")
    maintf_tab = MaintfstatusTable.objects.filter(is_maintf="true")
    if request.method == 'POST':
        print "POST!!!!"
        # 获得表单数据
        if 'productInfo' in request.POST.keys():
            print"into new report maintf"
            product = request.POST['productInfo']
            spm = request.POST['spmInfo']
            reporter = request.POST['reporterInfo']
            # 添加到数据库
            MaintfstatusTable.objects.create(product=product,
                                       spm=spm,
                                       daily_reporter=reporter
                                       )
        elif "idEdit" in request.POST.keys():
            print "into new report table"
            edit_id = request.POST['idEdit']
            edit_report = MaintfstatusTable.objects.get(id=edit_id)
            edit_report.product = request.POST['productEdit']
            edit_report.spm = request.POST['spmEdit']
            edit_report.daily_reporter = request.POST['reporterEdit']
            edit_report.save()
        elif 'delReportId' in request.POST.keys():
            print "into delete plan"
            del_id = request.POST['delReportId']
            del_report = MaintfstatusTable.objects.get(id=del_id)
            del_report.is_maintf = 'false'
            del_report.save()
        elif 'newHighId' in request.POST.keys():
            print"into new plan"
            for tab in plan_tab:
                requestid = int(tab.id)
                planid = 'newPlan%d' % requestid
                if planid in request.POST.keys():
                    tab.is_maintf = "true"
                    tab.is_high="true"
                    tab.save()
        elif 'newLowId' in request.POST.keys():
            print"into new plan"
            for tab in plan_tab:
                requestid = int(tab.id)
                planid = 'newPlan%d' % requestid
                if planid in request.POST.keys():
                    tab.is_maintf = "true"
                    tab.is_low = "true"
                    tab.save()
        elif 'delPlanId' in request.POST.keys():
            print "into delete plan"
            del_id = request.POST['delPlanId']
            del_plan = RequestTable.objects.get(id=del_id)
            del_plan.is_maintf = 'false'
            del_plan.is_high='false'
            del_plan.is_low='false'
            del_plan.save()
        else:
            print "there is something wrong"
        return HttpResponseRedirect('main_tf_status',{"plan_tab": plan_tab,"maintf_tab":maintf_tab,"is_maintf_tab":is_maintf_tab,"is_high_tab":is_high_tab,"is_low_tab":is_low_tab})
    else:
        print "GET!!!!"
        return render(request, 'report/main_tf_status.html',{"plan_tab": plan_tab,"maintf_tab":maintf_tab,"is_maintf_tab":is_maintf_tab,"is_high_tab":is_high_tab,"is_low_tab":is_low_tab})

def report_Schedule(request):
    schedule_tab = ScheduleTable.objects.filter(is_schedule="true").order_by("id")
    if request.method == 'POST':
        print "POST!!!!"
        # print request.body
        # 获得表单数据
        if 'productInfo' in request.POST.keys():
            print"into new schedule "
            handle_uploaded_file(request.FILES['file'], str(request.FILES['file']))
            product = request.POST['productInfo']
            spm = request.POST['spmInfo']
            reporter = request.POST['reporterInfo']
            file_link = str(request.FILES['file'])
            is_picture = False
            if ".jpg" or ".png" or ".gif" or ".bmp" or ".jpeg" in str(request.FILES['file']):
                is_picture = True
            # 添加到数据库
            ScheduleTable.objects.create(product=product,
                                       spm=spm,
                                       daily_reporter=reporter,
                                       file_link=file_link,
                                        is_picture=is_picture)
        elif 'productEdit' in request.POST.keys():
            print "edit schedule"
            edit_id = request.POST['idEdit']
            edit_schedule = ScheduleTable.objects.get(id=edit_id)
            edit_schedule.product = request.POST['productEdit']
            edit_schedule.spm = request.POST['spmEdit']
            edit_schedule.daily_reporter = request.POST['reporterEdit']
            if 'file_linkEdit' in request.FILES:
                handle_uploaded_file(request.FILES['file_linkEdit'], str(request.FILES['file_linkEdit']))
                edit_schedule.file_link = str(request.FILES['file_linkEdit'])
            edit_schedule.save()
        elif 'delReportId' in request.POST.keys():
            print "into delete plan"
            del_id = request.POST['delReportId']
            del_schedule = ScheduleTable.objects.get(id=del_id)
            del_schedule.is_schedule = 'false'
            del_schedule.save()
        else:
            print "there is something wrong"
        return HttpResponseRedirect('schedule', {"schedule_tab": schedule_tab})
    else:
        print "GET!!!!"
        return render(request, 'report/schedule.html', {"schedule_tab": schedule_tab})