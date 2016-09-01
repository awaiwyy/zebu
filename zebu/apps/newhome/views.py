#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect,StreamingHttpResponse
from common import com_def
from ..request.models import RequestTable
# Create your views here.
def newHomePage(request, **kwargs):
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
            server_ID = request.POST['serverId']
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
        return HttpResponseRedirect('/newhome/', {'valid_duration': valid_duration, "productlist": productlist})
    else:
        return render(request, 'newhome/newhome.html', {'valid_duration': valid_duration, "productlist": productlist})


