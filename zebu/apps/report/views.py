from django.shortcuts import render

# Create your views here.
def reportPage(request):
    return render(request, 'report/report.html')
	
def report_Resource(request):
    return render(request, 'report/resource_usage.html')

def report_MainTF(request):
    return render(request, 'report/main_tf_status.html')
	
def report_Schedule(request):
    return render(request, 'report/schedule.html')