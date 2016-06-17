#coding:utf-8
from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.http import HttpResponseRedirect
from models import RequestTable
import os
from common import xlwt

# Create your views here.
request_file = "resources/tab/request_tab.xls"

def saveRequestTab(request_tab):
    #set style
    font0 = xlwt.Font()
    font0.bold = True
    style0 = xlwt.XFStyle()
    style0.font = font0

    style = xlwt.XFStyle()
    style.num_format_str = 'YYYY-MM-DD'
    #creat sheet
    wb = xlwt.Workbook(encoding = 'utf-8')
    sheet = wb.add_sheet(u'request_tab', cell_overwrite_ok=True)

    row = 0  
    sheet.write(row, 0, 'ID', style0)
    sheet.write(row, 1, 'Project', style0)
    sheet.write(row, 2, 'TF Case', style0)
    sheet.write(row, 3, 'Classification', style0)
    sheet.write(row, 4, 'Module', style0)
    sheet.write(row, 5, 'Action Discription', style0)
    sheet.write(row, 6, 'Environment', style0)
    sheet.write(row, 7, 'Request Duration', style0)
    sheet.write(row, 8, 'Owner', style0)
    sheet.write(row, 9, 'Priority', style0)
    sheet.write(row, 10, 'Submit Date', style0)
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
        sheet.write(row, 10, tab.submit_date, style)
        row += 1
    wb.save(request_file)

def file_iterator(file_name, chunk_size=512):
    with open(file_name,"rb") as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break

def exportRequestTab(request):
    request_tab = RequestTable.objects.all().order_by("-submit_date")
    saveRequestTab(request_tab)
    file_name = request_file
    response = StreamingHttpResponse(file_iterator(file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(file_name)

    return response

def requestUser(request, **kwargs):
    #show request table
    request_tab = RequestTable.objects.all().order_by("-submit_date")
    #for request duration
    valid_duration = []
    valid_requestduration_piece = []
    valid_requestduration_day = []
    valid_requestduration_hour = []
    for day in range(1, 32):
        if day < 10:
            day = "0" + str(day)
        valid_requestduration_day.append(day)
    for hour in range(1, 25):
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
            request_duration = request.POST['durationHourEdit']+"Hour"+request.POST['durationDayEdit']+"Day"+request.POST['durationPieceEdit']+"Piece"
            owner = request.POST['ownerInfo']
            priority = request.POST['priorityInfo']
            #添加到数据库
            print [project, tf_case, classification, module, action_discription,
                   environment, request_duration, owner, priority]
            RequestTable.objects.create(project = project,
                                tf_case = tf_case,
                                classification = classification,
                                module = module,
                                action_discription = action_discription,
                                environment = environment,
                                request_duration = request_duration,
                                owner = owner,
                                priority = priority)
        elif 'idEdit' in request.POST.keys():
            print"into edit request tab"
            edit_id = request.POST['idEdit']
            edit_request = RequestTable.objects.get(id = edit_id)
            edit_request.project = request.POST['projectEdit']
            edit_request.tf_case = request.POST['tfcaseEdit']
            edit_request.classification = request.POST['classificationEdit']
            edit_request.module = request.POST['moduleEdit']
            edit_request.action_discription = request.POST['actionDiscriptionEdit']
            edit_request.environment = request.POST['environmentEdit']
            edit_request.request_duration = request.POST['requestDurationEdit']
            edit_request.owner = request.POST['ownerEdit']
            edit_request.priority = request.POST['priorityEdit']
            edit_request.save()
        elif 'delRqId' in request.POST.keys():
            print "into delete request tab"
            del_id = request.POST['delRqId']
            del_request = RequestTable.objects.get(id = del_id)
            del_request.delete()
        else:
            print "there is something wrong"
        #update request table
        #request_tab = RequestTable.objects.all().order_by("-submit_date")

        for tab in request_tab:
            tab.action_discription = tab.action_discription.replace("\n", "<br>")
        return HttpResponseRedirect('/request/', {"request_tab": request_tab, 'valid_duration': valid_duration}) #avoid submit twice when entering"F5"
    else:
        for tab in request_tab:
            tab.action_discription = tab.action_discription.replace("\n", "<br>")
        return render(request, 'request/request.html', {"request_tab": request_tab, 'valid_duration': valid_duration})