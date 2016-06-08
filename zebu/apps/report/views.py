from django.shortcuts import render
from models import ReportTable

# Create your views here.
def reportPage(request):
    daily_report_tab = ReportTable.objects.all()
    return render(request, 'report/report.html', {"daily_report_tab": daily_report_tab})
    #return render(request, 'report/report.html')

def report_Resource(request):
    return render(request, 'report/resource_usage.html')

def report_MainTF(request):
    return render(request, 'report/main_tf_status.html')

def report_Schedule(request):
    return render(request, 'report/schedule.html')