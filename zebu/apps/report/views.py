#coding:utf-8
from django.http import HttpResponseRedirect
from django.shortcuts import render
from models import ReportTable

# Create your views here.
def reportPage(request):
    daily_report_tab = ReportTable.objects.all()
    if request.method == 'POST':
        print"POST!!!!"
        #print request.body
        # 获得表单数据
        if 'productInfo' in request.POST.keys():
            print"into new daily report "
            product = request.POST['productInfo']
            spm = request.POST['spmInfo']
            reporter = request.POST['reporterInfo']
            # 添加到数据库
            ReportTable.objects.create(product=product,
                                       spm=spm,
                                       daily_reporter=reporter,
                                       file_link ="http://test.com/file")
        else:
            print "there is something wrong"
        return HttpResponseRedirect('/report/', {"daily_report_tab": daily_report_tab})
    else:
        print "GET!!!!"
        return render(request, 'report/report.html', {"daily_report_tab": daily_report_tab})
        #   return render(request, 'report/report.html')

def report_Resource(request):
    return render(request, 'report/resource_usage.html')

def report_MainTF(request):
    return render(request, 'report/main_tf_status.html')

def report_Schedule(request):
    return render(request, 'report/schedule.html')