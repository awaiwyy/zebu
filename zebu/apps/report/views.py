#coding:utf-8
from django.http import HttpResponseRedirect,StreamingHttpResponse
from django.shortcuts import render
from models import ReportTable
from models import ResourceUsageTable
from models import ResourceUsageTitleTable
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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
                                       file_link =file_link)
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
    #resource_usage_title_tab = ResourceUsageTitleTable.objects.all()
    resource_usage_tab = ResourceUsageTable.objects.filter(is_show="true").order_by("id")
    #resource_usage_tab = ResourceUsageTable.objects.all()
    return render(request, 'report/resource_usage.html',{"resource_usage_tab": resource_usage_tab})

def report_MainTF(request):
    return render(request, 'report/main_tf_status.html')

def report_Schedule(request):
    return render(request, 'report/schedule.html')