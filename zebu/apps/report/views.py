from django.shortcuts import render

# Create your views here.
def reportPage(request):
    return render(request, 'report/report.html')