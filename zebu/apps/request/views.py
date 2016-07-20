#coding:utf-8
from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from common import com_def
from models import RequestTable
from common import xlwt
import time,datetime
import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Create your views here.
temp_dir = os.path.join(BASE_DIR, "resources/tab/")
# Create your views here.
#temp_dir = "resources/tab/"
request_file = "request_tab.xls"

def saveRequestTab(request_tab,file_name):
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
    sheet.write(row, 1, 'Product', style0)
    sheet.write(row, 2, 'TF Case', style0)
    sheet.write(row, 3, 'Classification', style0)
    sheet.write(row, 4, 'Module', style0)
    sheet.write(row, 5, 'Action Discription', style0)
    sheet.write(row, 6, 'Environment', style0)
    sheet.write(row, 7, 'Request Duration', style0)
    sheet.write(row, 8, 'Owner', style0)
    sheet.write(row, 9, 'Priority', style0)
    sheet.write(row, 10, 'Submit Date', style0)
    sheet.write(row, 11, 'Acceptance', style0)
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
        sheet.write(row, 11, tab.acceptance, style)
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

    #Pagination -CC
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
                                priority = priority)
        elif 'idEdit' in request.POST.keys():
            #print"into edit request tab"
            edit_id = request.POST['idEdit']
            edit_request = RequestTable.objects.get(id = edit_id)
            edit_request.project = request.POST['projectEdit']
            edit_request.tf_case = request.POST['tfcaseEdit']
            edit_request.classification = request.POST['classificationEdit']
            edit_request.module = request.POST['moduleEdit']
            edit_request.action_discription = request.POST['actionDiscriptionEdit']
            edit_request.environment = request.POST['environmentEdit']
            edit_request.request_duration = request.POST['durationHourEdit']+"Hour"+request.POST['durationDayEdit']+"Day"+request.POST['durationPieceEdit']+"Piece"
            edit_request.owner = request.POST['ownerEdit']
            edit_request.priority = request.POST['priorityEdit']
            edit_request.save()
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
        return HttpResponseRedirect('/request/', {"request_tab": request_tab, 'valid_duration': valid_duration,"productlist":productlist}) #avoid submit twice when entering"F5"
    else:
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
        
        for tab in request_tab:
            tab.action_discription = tab.action_discription.replace("\n", "<br>")
        return render(request, 'request/request.html', {
            "request_tab": projects, 
            'valid_duration': valid_duration, 
            'range_left': range_left, 
            'range_right': range_right, 
            'over_range_left': over_range_left, 
            'over_range_right': over_range_right,
            "productlist": productlist})