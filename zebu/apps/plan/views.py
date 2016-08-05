# coding:utf-8
from django.shortcuts import render
from django.core.paginator import Page, EmptyPage, PageNotAnInteger, Paginator
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from ..request.models import RequestTable
from ..request.models import TotalTable
import time, datetime
from dateutil import tz
from common import com_def
from common import xlwt
import os
import json
import xlsxwriter
from common import sendEmail
from email.mime.text import MIMEText
from email.header import Header

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Create your views here.
temp_dir = os.path.join(BASE_DIR, "resources/tab/")
# Create your views here.
# temp_dir = "resources/tab/"
plan_file = "plan_tab.xlsx"


def savePlanTab(plan_tab, file_name):
    # creat sheet
    wb = xlsxwriter.Workbook(file_name)

    cell_format = wb.add_format({'bold': True, 'align': 'center', 'font': 'Arial', 'font_size': 10})
    style = wb.add_format({'bold': True, 'align': 'center', 'font': 'Arial', 'font_size': 10})  # 定义format格式对象
    style.set_num_format('yyyy-mm-dd')
    cell_format1 = wb.add_format({'align': 'center', 'font': 'Arial', 'font_size': 10})

    projectlist = RequestTable.objects.filter(is_plan="true")
    daily_tab1 = TotalTable.objects.all().order_by("change_date")
    sdate = daily_tab1[0].change_date
    daily_tab2 = TotalTable.objects.all().order_by("-change_date")
    cdate = daily_tab2[0].change_date
    dates = (cdate - sdate).days + 1
    project = []
    for tab in projectlist:
        project.append(tab.project)
    project = list(set(project))
    if len(project):
        for pro in project:
            sheet = wb.add_worksheet(pro)
            row = 0
            sheet.write(row, 0, 'ID', cell_format)
            sheet.write(row, 1, 'Product', cell_format)
            sheet.write(row, 2, 'Classification', cell_format)
            sheet.write(row, 3, 'Module', cell_format)
            sheet.write(row, 4, 'TF Case', cell_format)
            sheet.write(row, 5, 'Action Description', cell_format)
            sheet.write(row, 6, 'Environment', cell_format)
            sheet.write(row, 7, 'Total Duration', cell_format)
            sheet.write(row, 8, 'Owner', cell_format)
            sheet.write(row, 9, 'Priority', cell_format)
            sheet.write(row, 10, 'Status', cell_format)
            sheet.write(row, 11, 'Progress', cell_format)
            sheet.write(row, 12, 'Start Time', cell_format)
            sheet.write(row, 13, 'Request Duration', cell_format)
            sheet.write(row, 14, 'Close Time', cell_format)
            sheet.write(row, 15, 'Next Target', cell_format)
            sheet.write(row, 16, 'Acceptance', cell_format)
            sheet.write(row, 17, 'Server ID', cell_format)
            sheet.write(row, 18, 'Application Time', cell_format)
            sheet.set_column(1, 4, 13)
            sheet.set_column(5, 6, 15)
            sheet.set_column(7, 12, 10)
            sheet.set_column(13, 13, 18)
            sheet.set_column(14, 16, 10)
            sheet.set_column(17, 18, 16)

            for i in range(dates):
                sheet.set_column(19 + i, 19 + dates, 13)
                # sdate = datetime.datetime.strptime('2016-01-01', '%Y-%m-%d').date()
                date = sdate + datetime.timedelta(days=i)
                sheet.write(row, 19 + i, date, style)

            sheet.freeze_panes(1, 6)

            row += 1

            project_tab = RequestTable.objects.filter(is_plan="true", project=pro)
            for tab in project_tab:
                sheet.write(row, 0, tab.id, cell_format1)
                sheet.write(row, 1, tab.project, cell_format1)
                sheet.write(row, 2, tab.classification, cell_format1)
                sheet.write(row, 3, tab.module, cell_format1)
                sheet.write(row, 4, tab.tf_case, cell_format1)
                sheet.write(row, 5, tab.action_discription, cell_format1)
                sheet.write(row, 6, tab.environment, cell_format1)
                sheet.write(row, 7, tab.duration, cell_format1)
                sheet.write(row, 8, tab.owner, cell_format1)
                sheet.write(row, 9, tab.priority, cell_format1)
                sheet.write(row, 10, tab.status, cell_format1)
                sheet.write(row, 11, tab.progress, cell_format1)
                if tab.start_time:
                    sheet.write(row, 12, (tab.start_time + datetime.timedelta(hours=8)).strftime("%Y-%m-%d"))
                    daily_tab = TotalTable.objects.filter(request_id=tab.id).order_by("change_date")
                    for i in range(dates):
                        # sdate = datetime.datetime.strptime('2016-01-01', '%Y-%m-%d').date()
                        date = sdate + datetime.timedelta(days=i)
                        for tab1 in daily_tab:
                            if tab1.change_date == date:
                                sheet.write(row, 19 + i, tab1.daily_duration, cell_format1)
                else:
                    sheet.write(row, 12, (tab.start_time))
                sheet.write(row, 13, tab.request_duration, cell_format1)
                if tab.close_time:
                    sheet.write(row, 14, (tab.close_time + datetime.timedelta(hours=8)).strftime("%Y-%m-%d"))
                else:
                    sheet.write(row, 14, tab.close_time)
                sheet.write(row, 15, tab.next_target, cell_format1)
                sheet.write(row, 16, tab.acceptance, cell_format1)
                sheet.write(row, 17, tab.server_ID, cell_format1)
                if tab.application_time:
                    sheet.write(row, 18, (tab.application_time + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M"), cell_format1)
                row += 1
    wb.close()


def exportPlanTab(request):
    plan_tab = RequestTable.objects.filter(is_plan="true")
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
    # file_name = temp_dir + plan_file
    today = time.strftime("%Y_%m_%d", time.localtime())
    file_name = today + "_" + plan_file
    savePlanTab(plan_tab, file_name)
    f = open(file_name, "rb")
    data = f.read()
    f.close()

    response = HttpResponse(data)
    response['Content-Disposition'] = 'attachment; filename=%s' % file_name  # show download frame
    return response


def planPage(request, **kwargs):
    productlist = com_def.productlist[:]
    history_tab = TotalTable.objects.all().exclude(change_date=datetime.date.today()).order_by("change_date")
    gopage = request.GET.get('page')
    xxx = request.GET.get('status')

    if (gopage == None):
        gopage = "1"
    # show plan table
    request_tab = RequestTable.objects.filter(is_plan="false")
    plan_tab = RequestTable.objects.filter(is_plan="true").order_by("-id")
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
    # print valid_duration

    valid_dailyDura = []
    valid_dailyduration_piece = []
    valid_dailyduration_hour = []
    for hour in range(1, 25):
        if hour < 10:
            hour = "0" + str(hour)
        valid_dailyduration_hour.append(hour)
    for i in range(1, 11):
        if i < 10:
            piece = "0" + str(i)
        else:
            piece = i
        valid_dailyduration_piece.append(piece)
    valid_dailyDura.append(valid_dailyduration_hour)
    valid_dailyDura.append(valid_dailyduration_piece)
    # print valid_dailyDura

    valid_time = []
    valid_year = []
    valid_month = []
    valid_day = []
    valid_hour = []
    valid_min = []
    cur_year = datetime.datetime.now().year
    for year in range(cur_year - 5, cur_year + 10):
        valid_year.append(year)
    for month in range(1, 13):
        if month < 10:
            month = "0" + str(month)
        valid_month.append(month)
    for day in range(1, 32):
        if day < 10:
            day = "0" + str(day)
        valid_day.append(day)
    for hour in range(0, 24):
        if hour < 10:
            hour = "0" + str(hour)
        valid_hour.append(hour)
    for smin in range(0, 60):
        if smin < 10:
            smin = "0" + str(smin)
        valid_min.append(smin)
    valid_time.append(valid_year)
    valid_time.append(valid_month)
    valid_time.append(valid_day)
    valid_time.append(valid_hour)
    valid_time.append(valid_min)
    # print valid_time
    # add plan application

    # Pagination -CC
    perpage = 15  # show how many items per page

    objects = plan_tab
    pager = Paginator(objects, perpage)

    try:
        projects = pager.page(gopage)

    except PageNotAnInteger:
        projects = pager.page(1)
    except EmptyPage:
        projects = pager.page(pager.num_pages)

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

    # Range Left
    if (int(gopage) - 1 > pages_left):
        over_range_left = "true"
        range_left = range(int(gopage) - pages_left, int(gopage))
    if (int(gopage) - 1 == pages_left):
        range_left = range(1, int(gopage))
    if (int(gopage) - 1 < pages_left):
        range_left = range(1, int(gopage))

    # Range Right
    if (int(gopage) < pager.num_pages - pages_right):
        over_range_right = "true"
        range_right = range(int(gopage) + 1, int(gopage) + 1 + pages_right)
    if (int(gopage) == pager.num_pages - pages_right):
        range_right = range(int(gopage) + 1, int(gopage) + 1 + pages_right)
    if (int(gopage) > pager.num_pages - pages_right):
        range_right = range(int(gopage) + 1, pager.num_pages + 1)

    if request.method == 'POST':
        # 获得表单数据
        # print request.POST.keys()
        if 'newPlanId' in request.POST.keys():
            # print"into new plan"
            for tab in request_tab:
                requestid = int(tab.id)
                planid = 'newPlan%d' % requestid
                if planid in request.POST.keys():
                    tab.is_plan = "true"
                    tab.acceptance = "Yes"
                    tab.save()
        elif 'delPlanId' in request.POST.keys():
            # print "into delete plan"
            del_id = request.POST['delPlanId']
            del_plan = RequestTable.objects.get(id=del_id)
            del_plan.is_plan = 'false'
            del_plan.save()
        elif 'idEditCom' in request.POST.keys():
            # print "into common user edit plan"
            edit_id = request.POST['idEditCom']
            edit_plan = RequestTable.objects.get(id=edit_id)
            edit_plan.progress = request.POST['progressEditCom']
            edit_plan.save()
            # else:
            # print "there is something wrong"
        # update plan table
        request_tab = RequestTable.objects.filter(is_plan="false")
        plan_tab = RequestTable.objects.filter(is_plan="true").order_by("id")
        # print plan_tab

        for tab in plan_tab:
            tab.action_discription = tab.action_discription.replace("\n", "<br>")
            tab.progress = tab.progress.replace("\n", "<br>")
        return HttpResponseRedirect('/plan/',
                                    {"request_tab": request_tab, "plan_tab": plan_tab, 'valid_duration': valid_duration,
                                     'valid_time': valid_time, 'valid_dailyDura': valid_dailyDura,
                                     "history_tab": history_tab,"productlist":productlist})
    else:
        for tab in plan_tab:
            stime = tab.start_time
            if stime:
                stime = stime + datetime.timedelta(hours=8)
                ftimestr = stime.strftime('%Y-%m-%d %H:%M:%S')
                # print "ftimestr=",ftimestr
                ftime1 = ftimestr.split(' ')[0]
                ftime = datetime.datetime.strptime(ftime1, '%Y-%m-%d').date()
                # ftime = datetime.datetime.strptime(stime.strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S').date()
                # print "ftime=",ftime
                cur_time = datetime.date.today()
                # ctime = datetime.datetime.utcnow()
                # stime = datetime.datetime.strptime(stime.strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
                total = 0
                if "close" != tab.status:
                    if cur_time >= ftime:
                        total_tab1 = TotalTable.objects.filter(request_id=tab.id).order_by("-change_date")
                        if total_tab1:
                            recent_edit = total_tab1[0]
                            rtime = recent_edit.change_date
                            delta = (cur_time - rtime).days
                            # print "delta=",delta
                            # print "len(total_tab1)",len(total_tab1)
                            for i in range(delta):
                                # Totaltable中最大日期到今天相差天数的数据，按照前一天的数据补入：
                                # 1.若前一天状态为ongoing，当天的daily_duration值和前一天一样；
                                # 2.若前一天状态不是ongoing，当天的daily_duration值Hour为0，pieces为前一天daily_duration的pieces；
                                itime = rtime + datetime.timedelta(days=i + 1)
                                # print itime
                                try:
                                    lastday = total_tab1.get(change_date=(itime - datetime.timedelta(days=1)))
                                    daily_hour = tab.daily_duration.split('H')[0]
                                    daily_piece = tab.daily_duration.split('r')[1]
                                    if lastday.status == 'ongoing':
                                        TotalTable.objects.get_or_create(change_date=itime,
                                                                         daily_duration=daily_hour + "Hour" + daily_piece,
                                                                         status=lastday.status,
                                                                         request_id=lastday.request_id)
                                    else:
                                        TotalTable.objects.get_or_create(change_date=itime,
                                                                         daily_duration='00Hour' + daily_piece,
                                                                         status=lastday.status,
                                                                         request_id=lastday.request_id)
                                except:
                                    pass
                        else:
                            request_piece = tab.request_duration.split('y')[1]
                            delta = (cur_time - ftime).days
                            for i in range(delta):
                                itime = ftime + datetime.timedelta(days=i)
                                TotalTable.objects.create(change_date=itime,
                                                          daily_duration='00Hour' + request_piece,
                                                          status="ongoing",
                                                          request_id=tab.id)
                            daily_hour = tab.daily_duration.split('H')[0]
                            daily_piece = tab.daily_duration.split('r')[1]
                            TotalTable.objects.create(change_date=cur_time,
                                                      daily_duration=daily_hour + "Hour" + daily_piece,
                                                      status=tab.status,
                                                      request_id=tab.id)
                        i = 0
                        totaldelta = (cur_time - ftime).days
                        for i in range(totaldelta + 1):
                            itime = ftime + datetime.timedelta(days=i)
                            try:
                                curday = total_tab1.get(change_date=itime)
                                if curday.status == 'ongoing':
                                    idaily_h = int(curday.daily_duration.split('H')[0])
                                    idaily_p = int((curday.daily_duration.split('r')[1]).split('P')[0])
                                    total = total + idaily_h * idaily_p
                            except:
                                pass
                else:
                    total_tab1 = TotalTable.objects.filter(request_id=tab.id).order_by("-change_date")
                    ctime = tab.close_time
                    ctime = ctime + datetime.timedelta(hours=8)
                    ctimestr = ctime.strftime('%Y-%m-%d %H:%M:%S')
                    ctime1 = ctimestr.split(' ')[0]
                    ctime = datetime.datetime.strptime(ctime1, '%Y-%m-%d').date()
                    totaldelta1 = (ctime - ftime).days
                    i = 0
                    for i in range(totaldelta1 + 1):
                        # 计算total的值
                        itime = ftime + datetime.timedelta(days=i)
                        try:
                            curday = total_tab1.get(change_date=itime)
                            if curday.status == 'ongoing':
                                idaily_h = int(curday.daily_duration.split('H')[0])
                                idaily_p = int((curday.daily_duration.split('r')[1]).split('P')[0])
                                total = total + idaily_h * idaily_p
                        except:
                            pass
                tab.duration = total
                # 判断total值是否超过request的值
                request_h = int(tab.request_duration.split('H')[0])
                request_d = int((tab.request_duration.split('r')[1]).split('D')[0])
                request_p = int((tab.request_duration.split('y')[1]).split('P')[0])
                request_hours = request_h * request_d * request_p
                # print "request_hours" , request_hours
                if total >= request_hours:
                    tab.isdelay = 'delay'
                elif 'delay' == tab.isdelay:
                    tab.isdelay = 'no'
                    # request_hours= int(tab.request_duration.split('H')[0])
                    # real_duration = ctime - stime
                    # tab.duration = real_duration
                    # real_days = real_duration.days
                    # real_seconds = real_duration.seconds
                    # real_hours =real_days * 24 + real_seconds / 3600
                    # print "request hours: %d" % request_hours
                    # print "real hours: %d" % real_hours
                    # if real_hours >= request_hours:
                    # tab.status = 'delay'
                    # elif 'delay' == tab.status:
                    # tab.status = 'ongoing'
                tab.save()
            tab.action_discription = tab.action_discription.replace("\n", "<br>")
            tab.progress = tab.progress.replace("\n", "<br>")
        return render(request, 'plan/plan.html', {
            "request_tab": request_tab,
            "plan_tab": projects,
            'valid_duration': valid_duration,
            'valid_time': valid_time,
            'valid_dailyDura': valid_dailyDura,
            'range_left': range_left,
            'range_right': range_right,
            'over_range_left': over_range_left,
            'over_range_right': over_range_right,
            'history_tab': history_tab,
            "productlist":productlist})


def ajaxpost(request):
    # print "into edit plan"
    edit_id = request.POST['idEdit']
    edit_plan = RequestTable.objects.get(id=edit_id)
    total=edit_plan.duration
    utc_ctime=""
    edit_plan.project = request.POST['projectEdit']
    edit_plan.classification = request.POST['classificationEdit']
    edit_plan.module = request.POST['moduleEdit']
    edit_plan.tf_case = request.POST['tfcaseEdit']
    edit_plan.action_discription = request.POST['actionDiscriptionEdit']
    edit_plan.environment = request.POST['environmentEdit']
    # edit_plan.request_duration = request.POST['requestDurationEdit']
    edit_plan.priority = request.POST['priorityEdit']
    edit_plan.progress = request.POST['progressEdit']
    edit_plan.server_ID = request.POST['serverIdEdit']
    edit_plan.status = request.POST['statusEdit']
    # edit_stime = request.POST['startTimeEdit']

    # print "request_duration"
    valid_requestduration_piece = request.POST['durationPieceEdit']
    valid_requestduration_day = request.POST['durationDayEdit']
    valid_requestduration_hour = request.POST['durationHourEdit']
    request_dura = valid_requestduration_hour + "Hour" + valid_requestduration_day + "Day" + valid_requestduration_piece + "Piece"
    if request_dura != 'HourDayPiece':
        edit_plan.request_duration = request_dura
    # print request_dura

    # print "daily_duration"
    valid_dailyduration_piece = request.POST['dailyduraPieceEdit']
    valid_dailyduration_hour = request.POST['dailyduraHourEdit']
    if valid_dailyduration_piece and valid_dailyduration_hour:
        daily_dura = valid_dailyduration_hour + "Hour" + valid_dailyduration_piece + "Piece"
    else:
        valid_dailyduration_hour = str(0)
        valid_dailyduration_piece = request.POST['durationPieceEdit']
        daily_dura = valid_dailyduration_hour + "Hour" + valid_dailyduration_piece + "Piece"
    edit_plan.daily_duration = daily_dura
    print daily_dura

    change_date = datetime.date.today()
    daily_duration = daily_dura
    request_id = edit_id
    try:
        total_tab = TotalTable.objects.filter(request_id=request_id).get(change_date=change_date)
        total_tab.daily_duration = daily_dura
        total_tab.status = edit_plan.status
        total_tab.save()
    except:
        pass
        # print "not exist"
        # TotalTable.objects.create(change_date=change_date,
        #                           daily_duration=daily_duration,
        #                           status = edit_plan.status,
        #                           request_id=request_id)


        # total_duration
        # total_duration = RequestTable.objects.filter(is_plan="true").all()
        # for duration in total_duration:
        # print duration.request_duration.split('Hour ')[0]
        # print duration.request_duration.split('Hour')[1].split('Day')[0]
        # print duration.request_duration.split('Hour')[1].split('Day')[1].split('Piece')[0]

        # print "test_starttime"
    syear = request.POST['yearEdit']
    smonth = request.POST['monthEdit']
    sday = request.POST['dayEdit']
    shour = request.POST['hourEdit']
    sminute = request.POST['minuteEdit']
    ssecond = request.POST['secondEdit']
    edit_stime = syear + "-" + smonth + "-" + sday + " " + shour + ":" + sminute + ":" + ssecond
    cyear = request.POST['closeYearEdit']
    cmonth = request.POST['closeMonthEdit']
    cday = request.POST['closeDayEdit']
    chour = request.POST['closeHourEdit']
    cminute = request.POST['closeMinuteEdit']
    csecond = request.POST['closeSecondEdit']
    edit_ctime = cyear + "-" + cmonth + "-" + cday + " " + chour + ":" + cminute + ":" + csecond
    # 编辑每一天的daily_duration的值
    if 'arrId' in request.POST.keys():
        arrId=request.POST['arrId'].split(',')
        arrVal=request.POST['arrVal'].split(',')
        for id in range(len(arrId)):
            total_tab = TotalTable.objects.filter(request_id=edit_id).get(id=arrId[id])
            total_tab.daily_duration = arrVal[id]
        if request.POST['statusEdit'] != "close":
            total_tab.status = 'ongoing'
        total_tab.save()
    if edit_stime != '-- ::':
        stime = edit_stime.encode("utf-8")
        dtime = datetime.datetime.strptime(stime, '%Y-%m-%d %H:%M:%S')
        # fdate为starttime的日期
        fdate1 = (syear + "-" + smonth + "-" + sday).encode("utf-8")
        fdate = datetime.datetime.strptime(fdate1, '%Y-%m-%d').date()
        utc_time = dtime.replace(tzinfo=tz.gettz('CST'))
        edit_plan.start_time = utc_time
        # print dtime
        # print utc_time
        # cur_time = datetime.datetime.now()
        cur_time = datetime.date.today()
        # print "cur_time",cur_time
        total_tab1 = TotalTable.objects.filter(request_id=edit_plan.id).order_by("-change_date")
        total_tab2 = TotalTable.objects.filter(request_id=edit_plan.id).order_by("change_date")
        total = 0
        if cur_time > fdate:
            if not total_tab1:
                # 如果TotalTable里面没有数据即第一次编辑starttime时，当天的数据按照当天编辑的数据保存，之前的数据Hour为0，pieces为request_duration的pieces
                # total = 0
                request_piece = edit_plan.request_duration.split('y')[1]
                delta = (cur_time - fdate).days
                for i in range(delta):
                    itime = fdate + datetime.timedelta(days=i)
                    TotalTable.objects.create(change_date=itime,
                                              daily_duration='00Hour' + request_piece,
                                              status="ongoing",
                                              request_id=edit_plan.id)
                daily_hour = edit_plan.daily_duration.split('H')[0]
                daily_piece = edit_plan.daily_duration.split('r')[1]
                TotalTable.objects.create(change_date=cur_time,
                                          daily_duration=daily_hour + "Hour" + daily_piece,
                                          status=edit_plan.status,
                                          request_id=edit_plan.id)
                if edit_ctime != '-- ::':
                    Closedate1 = (cyear + "-" + cmonth + "-" + cday).encode("utf-8")
                    Closedate = datetime.datetime.strptime(Closedate1, '%Y-%m-%d').date()
                    ctime = edit_ctime.encode("utf-8")
                    dtime = datetime.datetime.strptime(ctime, '%Y-%m-%d %H:%M:%S')
                    utc_ctime = dtime.replace(tzinfo=tz.gettz('CST'))
                    edit_plan.close_time = utc_ctime
                    edit_plan.status = "close"
                    TotalTable.objects.filter(request_id=edit_plan.id, change_date__gt=Closedate).delete()
                    closedate = TotalTable.objects.get(request_id=edit_plan.id, change_date=Closedate)
                    closedate.status = "close"
                    closedate.save()
            else:
                first_edit = total_tab2[0]
                fedit = first_edit.change_date
                recent_edit = total_tab1[0]
                rtime = recent_edit.change_date
                if fdate < fedit:
                    # 如果starttime的日期在已有的最小日期之前，相差几天的数据Hour为0，pieces为request_duration的pieces,并存入TotalTable表
                    request_piece = edit_plan.request_duration.split('y')[1]
                    diffnum = (fedit - fdate).days
                    for j in range(diffnum):
                        itime = fdate + datetime.timedelta(days=j)
                        TotalTable.objects.create(change_date=itime,
                                                  daily_duration='00Hour' + request_piece,
                                                  status="ongoing",
                                                  request_id=edit_plan.id)
                elif fdate > fedit:
                    # 如果starttime的日期在已有的最小日期之后，多余的几天的数据就直接从TotalTable表中删除
                    total_tab2.filter(change_date__lt=fdate).delete()
                if edit_ctime == '-- ::':
                    # TotalTable中已经有当前记录的数据时，Totaltable中最大日期到今天相差天数的数据，按照前一天的数据补入：
                    # 1.若前一天状态为ongoing，当天的daily_duration值和前一天一样；
                    # 2.若前一天状态不是ongoing，当天的daily_duration值Hour为0，pieces为前一天daily_duration的pieces；
                    # total = 0
                    delta = (cur_time - rtime).days
                    totaldelta = (cur_time - fdate).days
                    for i in range(delta):
                        # print "i=", i
                        itime = rtime + datetime.timedelta(days=i + 1)
                        # print itime
                        try:
                            lastday = total_tab1.get(change_date=(itime - datetime.timedelta(days=1)))
                            daily_hour = edit_plan.daily_duration.split('H')[0]
                            daily_piece = edit_plan.daily_duration.split('r')[1]
                            if lastday.status == 'ongoing':
                                TotalTable.objects.get_or_create(change_date=itime,
                                                                 daily_duration=daily_hour + "Hour" + daily_piece,
                                                                 status=lastday.status,
                                                                 request_id=lastday.request_id)
                            else:
                                TotalTable.objects.get_or_create(change_date=itime,
                                                                 daily_duration='00Hour' + daily_piece,
                                                                 status=lastday.status,
                                                                 request_id=lastday.request_id)
                        except:
                            pass
                    i = 0
                    for i in range(totaldelta + 1):
                        # 计算total的值
                        itime = fdate + datetime.timedelta(days=i)
                        try:
                            curday = total_tab1.get(change_date=itime)
                            if curday.status == 'ongoing':
                                idaily_h = int(curday.daily_duration.split('H')[0])
                                idaily_p = int((curday.daily_duration.split('r')[1]).split('P')[0])
                                total = total + idaily_h * idaily_p
                        except:
                            pass
                else:
                    # fdate为starttime的日期
                    Closedate1 = (cyear + "-" + cmonth + "-" + cday).encode("utf-8")
                    Closedate = datetime.datetime.strptime(Closedate1, '%Y-%m-%d').date()
                    oldstatus = edit_plan.status
                    ctime = edit_ctime.encode("utf-8")
                    dtime = datetime.datetime.strptime(ctime, '%Y-%m-%d %H:%M:%S')
                    utc_ctime = dtime.replace(tzinfo=tz.gettz('CST'))
                    edit_plan.close_time = utc_ctime
                    if Closedate < rtime:
                        total_tab2.filter(change_date__gt=Closedate).delete()
                        closeitem = total_tab2.get(change_date=Closedate)
                        closeitem.status = 'close'
                        closeitem.save()
                    else:
                        if oldstatus == 'close':
                            olditem = TotalTable.objects.get(request_id=edit_plan.id, status="close")
                            olditem.status = "ongoing"
                            olditem.save()
                        delta1 = (Closedate - rtime).days
                        for i in range(delta1):
                            # print "i=", i
                            itime = rtime + datetime.timedelta(days=i + 1)
                            # print itime
                            try:
                                lastday = total_tab1.get(change_date=(itime - datetime.timedelta(days=1)))
                                daily_hour = edit_plan.daily_duration.split('H')[0]
                                daily_piece = edit_plan.daily_duration.split('r')[1]
                                if lastday.status == 'ongoing':
                                    TotalTable.objects.get_or_create(change_date=itime,
                                                                     daily_duration=daily_hour + "Hour" + daily_piece,
                                                                     status=lastday.status,
                                                                     request_id=lastday.request_id)
                                else:
                                    TotalTable.objects.get_or_create(change_date=itime,
                                                                     daily_duration='00Hour' + daily_piece,
                                                                     status=lastday.status,
                                                                     request_id=lastday.request_id)
                            except:
                                pass
                        closeitem = TotalTable.objects.get(request_id=edit_plan.id, change_date=Closedate)
                        closeitem.status = 'close'
                        closeitem.save()
                    totaldelta1 = (Closedate - fdate).days
                    i = 0
                    for i in range(totaldelta1 + 1):
                        # 计算total的值
                        itime = fdate + datetime.timedelta(days=i)
                        try:
                            curday = total_tab1.get(change_date=itime)
                            if curday.status == 'ongoing':
                                idaily_h = int(curday.daily_duration.split('H')[0])
                                idaily_p = int((curday.daily_duration.split('r')[1]).split('P')[0])
                                total = total + idaily_h * idaily_p
                        except:
                            pass
                    edit_plan.status = 'close'

        edit_plan.duration = total
        request_h = int(edit_plan.request_duration.split('H')[0])
        request_d = int((edit_plan.request_duration.split('r')[1]).split('D')[0])
        request_p = int((edit_plan.request_duration.split('y')[1]).split('P')[0])
        request_hours = request_h * request_d * request_p
        # print "request_hours", request_hours
        if total >= request_hours:
            edit_plan.isdelay = 'delay'
        elif 'delay' == edit_plan.isdelay:
            edit_plan.isdelay = 'no'

            # request_hour= int(edit_plan.request_duration.split('H')[0])
            # request_day= int (edit_plan.request_duration.split)
            # request_hours=request_hour+request_day*24
            # real_duration = cur_time - dtime
            # edit_plan.duration = real_duration
            # real_days = real_duration.days
            # real_seconds = real_duration.seconds
            # real_hours =real_days * 24 + real_seconds / 3600
            # print "request hours: %d" % request_hours
            # print "real hours: %d" % real_hours
            # if real_hours >= request_hours:
            # edit_plan.status = 'delay'
            # elif 'delay' == edit_plan.status:
            # edit_plan.status = 'ongoing'

            # print "next_target"
    next_target = request.POST['next_targetEdit']
    edit_plan.next_target = next_target
    edit_plan.save()
    #发邮件功能
    tf_case = request.POST['tfcaseEdit']
    owner = request.POST['ownerEdit']
    loginUser = request.POST['userInfo']
    #receivers = [owner+'@spreadtrum.com','nicole.wang@spreadtrum.com','chunsi.he@spreadtrum.com','chunji.chen@spreadtrum.com','fiona.zhang@spreadtrum.com','xinpeng.li@spreadtrum.com','guoliang.ren@spreadtrum.com']
    receivers = [owner+'@spreadtrum.com']
    #被处理的TF case/分配到的zebu/被分配使用的时间/操作者
    content = '被处理的TF case:'+tf_case+'/被分配使用的时间:'+edit_stime+'/操作者:'+loginUser
    subject = 'zebu资源已分配，请登录指定服务器和zebu处理'
    '''
    if sendEmail.send_mail(subject,content,receivers):
        print "send success"
    else:
        print"send fail"
       '''
    success_dict = {'edit_stime':edit_stime,
    'request_dura':request_dura,
    'daily_dura':daily_dura,
    'total':total,
    'utc_time': str(utc_ctime)}
    return HttpResponse(json.dumps(success_dict),
                        content_type="application/json")
