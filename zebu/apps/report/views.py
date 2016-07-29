#coding:utf-8
from __future__ import division
from django.http import HttpResponse
from django.http import HttpResponseRedirect,StreamingHttpResponse
from django.shortcuts import render
from models import ReportTable
from ..request.models import RequestTable
from common import com_def
from ..request.models import TotalTable
from models import ResourceUsageTable
from models import ResourceUsageTitleTable
from models import MaintfstatusTable
from models import ScheduleTable
import os
import math
import datetime
import json
from PIL import Image
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Create your views here.
upload_dir = os.path.join(BASE_DIR, "resources/upload/")
# "resources/upload/"
def reportPage(request):
    daily_report_tab = ReportTable.objects.filter(is_daily_report="true").order_by("id")
    #daily_report_tab = ReportTable.objects.all()
    productlist = com_def.productlist[:]
    for tab in daily_report_tab:
        if tab.product in productlist:
            productlist.remove(tab.product)
    if request.method == 'POST':
        #print "POST!!!!"
        #print request.body
        # 获得表单数据
        if 'productInfo' in request.POST.keys():
            #print"into new daily report "
            
            product = request.POST['productInfo']
            spm = request.POST['spmInfo']
            reporter = request.POST['reporterInfo']
            if "file" in request.FILES:
                file_link=str(request.FILES['file'])
                handle_uploaded_file(request.FILES['file'], str(request.FILES['file']))
            else:
                file_link=""
            # 添加到数据库
            ReportTable.objects.create(product=product,
                                       spm=spm,
                                       daily_reporter=reporter,
                                       file_link =file_link,
                                       )
        elif "idEdit" in request.POST.keys():
            #print "into new report table"
            edit_id = request.POST['idEdit']
            edit_report = ReportTable.objects.get(id=edit_id)
            edit_report.product = request.POST['productEdit']
            edit_report.spm = request.POST['spmEdit']
            edit_report.daily_reporter = request.POST['reporterEdit']
            deletefile = request.POST['deletefile']
            if deletefile:
                edit_report.is_picture = False
                edit_report.file_link = ""
            if 'file_linkEdit' in request.FILES:
                handle_uploaded_file(request.FILES['file_linkEdit'], str(request.FILES['file_linkEdit']))
                edit_report.file_link = str(request.FILES['file_linkEdit'])
            edit_report.save()
        elif 'delReportId' in request.POST.keys():
            #print "into delete plan"
            del_id = request.POST['delReportId']
            del_report = ReportTable.objects.get(id=del_id)
            del_report.is_daily_report = 'false'
            del_report.save()
        #else:
            #print "there is something wrong"
        return HttpResponseRedirect('daily_report', {"daily_report_tab": daily_report_tab, "productlist":productlist})
    else:
        #print "GET!!!!"
        return render(request, 'report/report.html', {"daily_report_tab": daily_report_tab, "productlist":productlist})
        #   return render(request, 'report/report.html')

def handle_uploaded_file(file, filename):
    if not os.path.exists(upload_dir):
        os.mkdir(upload_dir)
    with open(upload_dir + filename.decode('utf-8'), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    pic_list=["jpg","png","gif","bmp","jpeg"]
    if filename.split(".")[-1].lower() in pic_list:
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
        response['Content-Disposition'] = 'attachment;filename="{0}"'.format(filename)
        return response

def report_Resource(request):
    date_changed=""
    tf_list=['Power','Performance','Fun','ZEBU']
    plan_tab=RequestTable.objects.filter(is_plan="true",status="ongoing").order_by("id")
    total_tab1=TotalTable.objects.order_by("-change_date","-id")
    title_tab = ResourceUsageTitleTable.objects.all()
    resource_usage_tab = ResourceUsageTable.objects.filter(is_show="true").order_by("id")
    #find first edit date of TotalTable.
    fedit="2000-01-01"
    edit_date="2000-01-01"
    edit_id="-1"
    try:
        first_edit=total_tab1[0]
        fedit=first_edit.change_date
    except:
        pass
    #create '0~20' list for html pull-down list.
    totalitem=[]
    for hour in range(21):
        if hour < 10:
            hour = "0" + str(hour)
        totalitem.append(hour)
    #remove page exist products from new product list.
    productlist = com_def.productlist[:]
    for tab in resource_usage_tab:
        if tab.product in productlist:
            productlist.remove(tab.product)
    if request.method == 'POST':
        #print "POST!!!!"
        # 获得表单数据
        if 'productInfo' in request.POST.keys():
            product = request.POST['productInfo']
            spm = request.POST['spmInfo']
            reporter = request.POST['reporterInfo']
            usagelist=[]
            usage=[]
            for tf in tf_list:
                #collect plan page ids which product name same as resource usage page,and classify by tf_case.
                res_plan_tab=plan_tab.filter(project=product,tf_case__startswith=tf)
                idlist=[]
                for tab1 in res_plan_tab:
                    idlist.append(tab1.id)
                #collect TotalTable daily duration data of recent edit which id in idlist.
                total_tab_all=TotalTable.objects.filter(request_id__in=idlist).order_by("-change_date","-id")
                total_tab=total_tab_all.filter(change_date=fedit)
                #calculate each tf_case value
                totalusage=0
                for tab in total_tab:
                    daily_usage=int(tab.daily_duration.split('H')[0])*int(tab.daily_duration.split('r')[1].split('P')[0])
                    totalusage=totalusage+daily_usage
                usagelist=[tf,totalusage]
                usage.append(usagelist)
            #calculate sum and average of four tf_case
            sum=0
            avg=0
            for j in range(4):
                sum=sum+usage[j][1]
            avg=int(math.ceil(sum/24)) 
            # 添加到数据库
            try:
                ResourceUsageTable.objects.create(product=product,
                                                spm=spm,
                                                daily_reporter=reporter,
                                                choosedate=datetime.date.today(),
                                                total=avg*24,
                                                power_management=usage[0][1],
                                                performance=usage[1][1],
                                                function=usage[2][1],
                                                zebu_platform=usage[3][1] 
                                                )
            except:
                pass
                                            
        elif 'edittotal0' in request.POST.keys():
            #print "edit total and usage"
            edit_id = request.POST["idEdit110"]
            #print edit_id
            total = int(request.POST["edittotal0"])*24
            usage = int(request.POST["editusage0"])*24
            ResourceUsageTitleTable.objects.create(usage=usage,
                                                   total=total)
        elif 'edittotal' in request.POST.keys():
            #print "edit total and usage"
            edit_id =request.POST["idEdit11" ]
            #print edit_id
            total = int(request.POST["edittotal"])*24
            usage = int(request.POST["editusage"])*24
            edittitle_tab = ResourceUsageTitleTable.objects.get(id=edit_id)
            edittitle_tab.total= total
            edittitle_tab.usage = usage
            edittitle_tab.save()
        elif 'productEdit' in request.POST.keys():
            edit_id = request.POST['idEdit']
            edit_resource = ResourceUsageTable.objects.get(id=edit_id)
            Pro_product = edit_resource.product
            edit_resource.product = request.POST['productEdit']
            if Pro_product != edit_resource.product:
                ResourceUsageTable.objects.filter(product=Pro_product).delete()
                edit_resource.product = request.POST['productEdit']
                edit_resource.spm = request.POST['spmEdit']
                edit_resource.daily_reporter = request.POST['reporterEdit']
                edit_resource.total = int(request.POST['totalEdit']) * 24
                edit_resource.save()
            else:
                edit_product = request.POST['productEdit']
                edit_date = request.POST['showchoosedate']
                edit_resource1 = ResourceUsageTable.objects.get(is_show="true",product=edit_product,choosedate=edit_date)
                edit_resource1.spm = request.POST['spmEdit']
                edit_resource1.daily_reporter = request.POST['reporterEdit']
                total1=edit_resource1.total
                edit_resource1.total = int(request.POST['totalEdit'])*24
                total2 = edit_resource1.total
                if total1 != total2:
                   edit_resource1.is_edit = "true"
                edit_resource1.save()
        elif 'delresourceId' in request.POST.keys():
            del_id = request.POST['delresourceId']
            del_product=ResourceUsageTable.objects.get(id=del_id).product
            ResourceUsageTable.objects.filter(product=del_product).update(is_show="false")
        date_changed =  edit_date
        resource_usage_tab = ResourceUsageTable.objects.filter(is_show="true", choosedate=fedit).order_by("id")
        
        #return HttpResponseRedirect('resource_usage', {"date_changed": date_changed, "resource_usage_tab":  resource_usage_tab,"title_tab": title_tab,"totalitem":totalitem,"productlist":productlist,"fedit":fedit})
        return render(request, 'report/resource_usage.html',
                        {"product_changed": int(edit_id),
                        "date_changed":date_changed, 
                        "resource_usage_tab": resource_usage_tab,
                        "title_tab": title_tab,
                        "productlist":productlist,
                        "totalitem":totalitem,
                        "fedit":fedit})

    else:
        #print "GET!!!!"
        usagelist=[]
        restablist=[]
        #list all product on resource usage page.
        for restab in resource_usage_tab:
            restablist.append(restab.product)
        relist=list(set(restablist))
        #collect plan page daily duration sum which product name same as resource usage page classify by tf_case.
        for product in relist:
            usagetotallist=[]
            avglist=[]
            for tf in tf_list:
                res_plan_tab=plan_tab.filter(project=product,tf_case__startswith=tf)
                idlist=[]
                for tab1 in res_plan_tab:
                    idlist.append(tab1.id)
                total_tab_all=TotalTable.objects.filter(request_id__in=idlist).order_by("-change_date","-id")
                total_tab=total_tab_all.filter(change_date=fedit)
                totalusage=0
                for tab in total_tab:
                    print tab.daily_duration
                    daily_usage=int(tab.daily_duration.split('H')[0])*int(tab.daily_duration.split('r')[1].split('P')[0])
                    totalusage=totalusage+daily_usage
                usagelist=[tf,totalusage]
                usagetotallist.append({'pro':product,'data':usagelist})
            #calculate sum and average of four tf_case
            sum=0
            avg=0
            for j in range(4):
                sum=sum+usagetotallist[j]['data'][1]
            avg=int(math.ceil(sum/24))
            avglist.append({'pro':product,'data':avg})
            # 添加到数据库
            try:
                #update
                refresh_tab = resource_usage_tab.get(product=product,choosedate=fedit)
                refresh_tab.power_management = usagetotallist[0]['data'][1]
                refresh_tab.performance = usagetotallist[1]['data'][1]
                refresh_tab.function = usagetotallist[2]['data'][1]
                refresh_tab.zebu_platform = usagetotallist[3]['data'][1]
                totalsum=refresh_tab.power_management+refresh_tab.performance+refresh_tab.function+refresh_tab.zebu_platform
                if refresh_tab.total < totalsum:
                    refresh_tab.is_edit = 'false'
                if refresh_tab.is_edit == 'false':
                    refresh_tab.total = avglist[0]['data'] * 24
                refresh_tab.save()
            except:
                #new
                example_usage_tab=resource_usage_tab.filter(product=product).order_by('-choosedate')
                spm=example_usage_tab[0].spm
                reporter=example_usage_tab[0].daily_reporter
                ResourceUsageTable.objects.get_or_create(product=product,
                                                spm=spm,
                                                daily_reporter=reporter,
                                                choosedate=fedit,
                                                total=avglist[0]['data']*24,
                                                power_management = usagetotallist[0]['data'][1],
                                                performance = usagetotallist[1]['data'][1],
                                                function = usagetotallist[2]['data'][1],
                                                zebu_platform = usagetotallist[3]['data'][1])
        resource_usage_tab = ResourceUsageTable.objects.filter(is_show="true",choosedate=fedit).order_by("id")
        return render(request, 'report/resource_usage.html',{"product_changed": "notcheck","resource_usage_tab": resource_usage_tab,"title_tab": title_tab,"productlist":productlist,"totalitem":totalitem,"fedit":fedit})


def report_MainTF(request):
    plan_tab = RequestTable.objects.filter(is_plan="true",is_maintf="false")
    is_maintf_tab=RequestTable.objects.filter(is_plan="true",is_maintf="true")
    is_high_tab=is_maintf_tab.filter(is_high="true")
    is_low_tab = is_maintf_tab.filter(is_low="true")
    maintf_tab = MaintfstatusTable.objects.filter(is_maintf="true").order_by("id")
    productlist = com_def.productlist[:]
    for tab in maintf_tab:
        if tab.product in productlist:
            productlist.remove(tab.product)
    if request.method == 'POST':
        #print "POST!!!!"
        # 获得表单数据
        if 'productInfo' in request.POST.keys():
            #print"into new report maintf"
            product = request.POST['productInfo']
            spm = request.POST['spmInfo']
            reporter = request.POST['reporterInfo']
            # 添加到数据库
            MaintfstatusTable.objects.create(product=product,
                                       spm=spm,
                                       daily_reporter=reporter
                                       )
        elif "idEdit" in request.POST.keys():
            #print "into new report table"
            edit_id = request.POST['idEdit']
            edit_report = MaintfstatusTable.objects.get(id=edit_id)
            edit_report.product = request.POST['productEdit']
            edit_report.spm = request.POST['spmEdit']
            edit_report.daily_reporter = request.POST['reporterEdit']
            edit_report.save()
        elif 'delReportId' in request.POST.keys():
            #print "into delete plan"
            del_id = request.POST['delReportId']
            del_report = MaintfstatusTable.objects.get(id=del_id)
            del_report.is_maintf = 'false'
            del_report.save()
        elif 'newHighId' in request.POST.keys():
            #print"into new plan"
            for tab in plan_tab:
                requestid = int(tab.id)
                planid = 'newPlan%d' % requestid
                if planid in request.POST.keys():
                    tab.is_maintf = "true"
                    tab.is_high="true"
                    tab.save()
        elif 'newLowId' in request.POST.keys():
            #print"into new plan"
            for tab in plan_tab:
                requestid = int(tab.id)
                planid = 'newPlan%d' % requestid
                if planid in request.POST.keys():
                    tab.is_maintf = "true"
                    tab.is_low = "true"
                    tab.save()
        elif 'delPlanId' in request.POST.keys():
            #print "into delete plan"
            del_id = request.POST['delPlanId']
            del_plan = RequestTable.objects.get(id=del_id)
            del_plan.is_maintf = 'false'
            del_plan.is_high='false'
            del_plan.is_low='false'
            del_plan.save()
        #else:
            #print "there is something wrong"
        return HttpResponseRedirect('main_tf_status',{"plan_tab": plan_tab,"maintf_tab":maintf_tab,"is_maintf_tab":is_maintf_tab,"is_high_tab":is_high_tab,"is_low_tab":is_low_tab,"productlist":productlist})
    else:
        #print "GET!!!!"
        return render(request, 'report/main_tf_status.html',{"plan_tab": plan_tab,"maintf_tab":maintf_tab,"is_maintf_tab":is_maintf_tab,"is_high_tab":is_high_tab,"is_low_tab":is_low_tab,"productlist":productlist})

def report_Schedule(request):





    schedule_tab = ScheduleTable.objects.filter(is_schedule="true").order_by("id")
    productlist = com_def.productlist[:]
    for tab in schedule_tab:
        if tab.product in productlist:
            productlist.remove(tab.product)
    if request.method == 'POST':
        #print "POST!!!!"
        # print request.body
        # 获得表单数据
        if 'productInfo' in request.POST.keys():
            #print"into new schedule "
            product = request.POST['productInfo']
            spm = request.POST['spmInfo']
            reporter = request.POST['reporterInfo']
            pic_list=["jpg","png","gif","bmp","jpeg"]
            is_picture = False
            if "file" in request.FILES:
                file_link=str(request.FILES['file'])
                handle_uploaded_file(request.FILES['file'], str(request.FILES['file']))
                if file_link.split(".")[-1].lower() in pic_list:
                    is_picture = True
            else:
                file_link=""
            # 添加到数据库
            ScheduleTable.objects.create(product=product,
                                       spm=spm,
                                       daily_reporter=reporter,
                                       file_link=file_link,
                                        is_picture=is_picture)
        elif 'productEdit' in request.POST.keys():
            #print "edit schedule"
            edit_id = request.POST['idEdit']
            edit_schedule = ScheduleTable.objects.get(id=edit_id)
            edit_schedule.product = request.POST['productEdit']
            edit_schedule.spm = request.POST['spmEdit']
            edit_schedule.daily_reporter = request.POST['reporterEdit']
            deletefile = request.POST['deletefile']
            pic_list = ["jpg", "png", "gif", "bmp", "jpeg"]
            if deletefile:
                edit_schedule.is_picture = False
                edit_schedule.file_link = ""
            if 'file_linkEdit' in request.FILES:
                file_link = str(request.FILES['file_linkEdit'])
                handle_uploaded_file(request.FILES['file_linkEdit'], str(request.FILES['file_linkEdit']))
                if file_link.split(".")[-1].lower() in pic_list:
                    edit_schedule.is_picture = True
                else:
                    edit_schedule.is_picture = False
                edit_schedule.file_link = str(request.FILES['file_linkEdit'])
            edit_schedule.save()
        elif 'delattId' in request.POST.keys():
            #print "delete attachment"
            del_id = request.POST['delattId']
            del_schedule = ScheduleTable.objects.get(id=del_id)
            del_schedule.is_picture = False
            del_schedule.file_link = ""
            del_schedule.save()
        elif 'delReportId' in request.POST.keys():
            #print "into delete plan"
            del_id = request.POST['delReportId']
            del_schedule = ScheduleTable.objects.get(id=del_id)
            del_schedule.is_schedule = 'false'
            del_schedule.save()
        #else:
            #print "there is something wrong"
        return HttpResponseRedirect('schedule', {"schedule_tab": schedule_tab,"productlist":productlist})
    else:
        #print "GET!!!!"
        return render(request, 'report/schedule.html', {"schedule_tab": schedule_tab,"productlist":productlist})

def ajaxget(request):
    #get datepicker checked date and id.
    getproductid = int(request.GET['productid'])
    getdate = request.GET['date'].replace(".","-")
    edit_product = ResourceUsageTable.objects.get(id=getproductid).product
    #collect plan page daily duration sum which product name same as resource usage page classify by tf_case.
    tf_list=['Power','Performance','Fun','ZEBU']
    plan_tab=RequestTable.objects.filter(is_plan="true",status="ongoing").order_by("id")
    resource_usage_tab = ResourceUsageTable.objects.filter(is_show="true",product=edit_product).order_by('-choosedate')
    usagelist=[]
    usage=[]
    for tf in tf_list:
        res_plan_tab=plan_tab.filter(project=edit_product,tf_case__startswith=tf)
        idlist=[]
        for tab1 in res_plan_tab:
            idlist.append(tab1.id)
        total_tab_all=TotalTable.objects.filter(request_id__in=idlist).order_by("-change_date","-id")
        total_tab=total_tab_all.filter(change_date=getdate)
        totalusage=0
        for tab in total_tab:
            daily_usage=int(tab.daily_duration.split('H')[0])*int(tab.daily_duration.split('r')[1].split('P')[0])
            totalusage=totalusage+daily_usage
        usagelist=[tf,totalusage]
        usage.append(usagelist)
    #calculate sum and average of four tf_case
    sum=0
    avg=0
    for j in range(4):
        sum=sum+usage[j][1]
    avg=int(math.ceil(sum/24)) 

    # 添加到数据库
    try:
        #update
        refresh_tab = resource_usage_tab.get(choosedate=getdate)        
        refresh_tab.power_management = usage[0][1]
        refresh_tab.performance = usage[1][1]
        refresh_tab.function = usage[2][1]
        refresh_tab.zebu_platform = usage[3][1]
        totalsum=refresh_tab.power_management+refresh_tab.performance+refresh_tab.function+refresh_tab.zebu_platform
        if refresh_tab.total < totalsum:
            refresh_tab.is_edit = 'false'
        if refresh_tab.is_edit == 'false':
            refresh_tab.total = avg * 24
        refresh_tab.save()
    except:
        #new
        spm=resource_usage_tab[0].spm
        reporter=resource_usage_tab[0].daily_reporter
        ResourceUsageTable.objects.get_or_create(product=edit_product,
                                                spm=spm,
                                                daily_reporter=reporter,
                                                choosedate=getdate,
                                                total=avg*24,
                                                power_management=usage[0][1],
                                                performance=usage[1][1],
                                                function=usage[2][1],
                                                zebu_platform=usage[3][1] )

    edit_tab=ResourceUsageTable.objects.get(is_show="true",choosedate=getdate,product=edit_product)
    #transmit ResourceUsageTable data to webpage.
    product=edit_tab.product
    spm=edit_tab.spm
    daily_reporter=edit_tab.daily_reporter
    total=edit_tab.total
    power_management=edit_tab.power_management
    performance=edit_tab.performance
    function=edit_tab.function
    zebu_platform=edit_tab.zebu_platform
    edit_dict = {'product':product,
                'spm':spm,
                'daily_reporter':daily_reporter,
                 'total': total,
                 'power_management': power_management,
                 'performance':performance,
                 'function':function,
                 'zebu_platform':zebu_platform
                 }
    return HttpResponse(json.dumps(edit_dict),
                    content_type="application/json")


def ajaxpost(request):
    date = request.POST['showchoosedate']
    product = request.POST['productEdit']
    spm = request.POST['spmEdit']
    total = request.POST['totalEdit']
    edit_id = request.POST['idEdit']
    edit_resource = ResourceUsageTable.objects.get(id=edit_id)
    Pro_product = edit_resource.product
    edit_resource.product = request.POST['productEdit']
    if Pro_product != edit_resource.product:
        ResourceUsageTable.objects.filter(product=Pro_product).delete()
        edit_resource.product = request.POST['productEdit']
        edit_resource.spm = request.POST['spmEdit']
        edit_resource.daily_reporter = request.POST['reporterEdit']
        edit_resource.total = int(request.POST['totalEdit']) * 24
        edit_resource.save()
    else:
        edit_product = request.POST['productEdit']
        edit_date = request.POST['showchoosedate']
        edit_resource1 = ResourceUsageTable.objects.get(is_show="true", product=edit_product, choosedate=edit_date)
        edit_resource1.spm = request.POST['spmEdit']
        edit_resource1.daily_reporter = request.POST['reporterEdit']
        total1 = edit_resource1.total
        edit_resource1.total = int(request.POST['totalEdit']) * 24
        total2 = edit_resource1.total
        if total1 != total2:
            edit_resource1.is_edit = "true"
        edit_resource1.save()
        edit_resource1.save()
    success_dict = {}
    return HttpResponse(json.dumps(success_dict),
                        content_type="application/json")