#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from ..request.models import RequestTable
from ..request.models import TotalTable
import datetime
from dateutil import tz
from common import xlwt

# Create your views here.
plan_file = "resources/tab/plan_tab.xls"
def savePlanTab(plan_tab):
    #set style
    font0 = xlwt.Font()
    font0.bold = True
    style0 = xlwt.XFStyle()
    style0.font = font0

    #creat sheet
    wb = xlwt.Workbook(encoding = 'utf-8')
    sheet = wb.add_sheet(u'plan_tab', cell_overwrite_ok=True)

    row = 0  
    sheet.write(row, 0, 'ID', style0)
    sheet.write(row, 1, 'Project', style0)
    sheet.write(row, 2, 'Classification', style0)
    sheet.write(row, 3, 'Module', style0)
    sheet.write(row, 4, 'TF Case', style0)
    sheet.write(row, 5, 'Action Discription', style0)
    sheet.write(row, 6, 'Environment', style0)
    sheet.write(row, 7, 'Duration', style0)
    sheet.write(row, 8, 'Owner', style0)
    sheet.write(row, 9, 'Priority', style0)
    sheet.write(row, 10, 'Status', style0)
    sheet.write(row, 11, 'Progress', style0)
    sheet.write(row, 12, 'Start Time', style0)
    sheet.write(row, 13, 'Request Duration', style0)
    row += 1
    
    for tab in plan_tab:
        sheet.write(row, 0, tab.id)
        sheet.write(row, 1, tab.project)
        sheet.write(row, 2, tab.classification)
        sheet.write(row, 3, tab.module)
        sheet.write(row, 4, tab.tf_case)
        sheet.write(row, 5, tab.action_discription)
        sheet.write(row, 6, tab.environment)
        sheet.write(row, 7, tab.duration)
        sheet.write(row, 8, tab.owner)
        sheet.write(row, 9, tab.priority)
        sheet.write(row, 10, tab.status)
        sheet.write(row, 11, tab.progress)
        if tab.start_time:
            sheet.write(row, 12, (tab.start_time + datetime.timedelta(hours=8)).strftime("%Y-%m-%d %H:%M:%S"))
        else:
            sheet.write(row, 12, (tab.start_time))
        sheet.write(row, 13, tab.request_duration)
        row += 1
    wb.save(plan_file)

def exportPlanTab(request):
    plan_tab = RequestTable.objects.filter(is_plan="true")
    savePlanTab(plan_tab)
    file_name = plan_file
    f = open(file_name)
    data = f.read()
    f.close()
 
    response = HttpResponse(data)   
    response['Content-Disposition'] = 'attachment; filename=%s' % file_name #show download frame
    return response

def planPage(request, **kwargs):
    #show plan table
    request_tab = RequestTable.objects.filter(is_plan="false")
    plan_tab = RequestTable.objects.filter(is_plan="true").order_by("id")
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
            hour="0" + str(hour)
        valid_requestduration_hour.append(hour)
    for i in range(1, 11):
        if i < 10:
            piece = "0" +str(i)
        else:
            piece=i
        valid_requestduration_piece.append(piece)
    valid_duration.append(valid_requestduration_hour)
    valid_duration.append(valid_requestduration_day)
    valid_duration.append(valid_requestduration_piece)
    #print valid_duration
    
    valid_dailyDura = []
    valid_dailyduration_piece = []
    valid_dailyduration_hour = []
    for hour in range(1, 25):
        if hour < 10:
            hour="0"+str(hour)
        valid_dailyduration_hour.append(hour)
    for i in range(1, 11):
        if i < 10:
            piece = "0" +str(i)
        else:
            piece = i
        valid_dailyduration_piece.append(piece)
    valid_dailyDura.append(valid_dailyduration_hour)
    valid_dailyDura.append(valid_dailyduration_piece)
    print valid_dailyDura

    valid_time = []
    valid_year = []
    valid_month = []
    valid_day = []
    valid_hour = []
    valid_min = []
    cur_year = datetime.datetime.now().year
    for year in range(cur_year-5, cur_year+10):
        valid_year.append(year)
    for month in range(1, 13):
        if month <10:
            month = "0"+str(month)
        valid_month.append(month)
    for day in range(1, 32):
        if day<10:
            day = "0"+str(day)
        valid_day.append(day)
    for hour in range(0, 24):
        if hour<10:
            hour="0"+str(hour)
        valid_hour.append(hour)
    for smin in range(0, 60):
        if smin<10:
            smin="0"+str(smin)
        valid_min.append(smin)
    valid_time.append(valid_year)
    valid_time.append(valid_month)
    valid_time.append(valid_day)
    valid_time.append(valid_hour)
    valid_time.append(valid_min)
    #print valid_time
    #add plan application
    if request.method == 'POST':
        #获得表单数据
        print request.POST.keys()
        if 'newPlanId' in request.POST.keys():
            print"into new plan"
            for tab in request_tab:
                requestid = int(tab.id)
                planid = 'newPlan%d' % requestid
                if planid in request.POST.keys():
                    tab.is_plan = "true"
                    tab.save()
        elif 'idEdit' in request.POST.keys():
            print "into edit plan"
            edit_id = request.POST['idEdit']
            edit_plan = RequestTable.objects.get(id=edit_id)
            edit_plan.project = request.POST['projectEdit']
            edit_plan.classification = request.POST['classificationEdit']
            edit_plan.module = request.POST['moduleEdit']
            edit_plan.tf_case = request.POST['tfcaseEdit']
            edit_plan.action_discription = request.POST['actionDiscriptionEdit']
            edit_plan.environment = request.POST['environmentEdit']
            #edit_plan.request_duration = request.POST['requestDurationEdit']
            edit_plan.owner = request.POST['ownerEdit']
            edit_plan.priority = request.POST['priorityEdit']
            edit_plan.progress = request.POST['progressEdit']
            edit_plan.status = request.POST['statusEdit']
            #edit_stime = request.POST['startTimeEdit']
            
            print "request_duration"
            valid_requestduration_piece = request.POST['durationPieceEdit']
            valid_requestduration_day = request.POST['durationDayEdit']
            valid_requestduration_hour = request.POST['durationHourEdit']
            request_dura = valid_requestduration_hour+"Hour"+valid_requestduration_day+"Day"+valid_requestduration_piece+"Piece"
            if request_dura != 'HourDayPiece':
                edit_plan.request_duration = request_dura
            print request_dura
            
            print "daily_duration"
            valid_dailyduration_piece = request.POST['dailyduraPieceEdit']
            valid_dailyduration_hour = request.POST['dailyduraHourEdit']
            if valid_dailyduration_piece and valid_dailyduration_hour:
                daily_dura = valid_dailyduration_hour + "Hour" + valid_dailyduration_piece + "Piece"
            else:
                valid_dailyduration_hour = str(24)
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
                print "not exist"
                TotalTable.objects.create(change_date=change_date,
                                          daily_duration=daily_duration,
                                          status = edit_plan.status,
                                          request_id=request_id)

            
            #total_duration
            #total_duration = RequestTable.objects.filter(is_plan="true").all()
            #for duration in total_duration:
                #print duration.request_duration.split('Hour ')[0]
                #print duration.request_duration.split('Hour')[1].split('Day')[0]
                #print duration.request_duration.split('Hour')[1].split('Day')[1].split('Piece')[0]
                
            print "test_starttime"
            year = request.POST['yearEdit']
            month = request.POST['monthEdit']
            day = request.POST['dayEdit']
            hour = request.POST['hourEdit']
            minute = request.POST['minuteEdit']
            second = request.POST['secondEdit']
            edit_stime = year+"-"+month+"-"+day+" "+hour+":"+minute+":"+second
            if edit_stime != '-- ::' and 'close' != edit_plan.status:
                stime = edit_stime.encode("utf-8")
                dtime = datetime.datetime.strptime(stime,'%Y-%m-%d %H:%M:%S')
                ftime1 = (year+"-"+month+"-"+day).encode("utf-8")
                ftime = datetime.datetime.strptime(ftime1,'%Y-%m-%d').date()
                utc_time = dtime.replace(tzinfo=tz.gettz('CST'))

                print dtime
                print "ftime:",ftime
                print utc_time
                #cur_time = datetime.datetime.now()
                cur_time = datetime.date.today()
                print "cur_time",cur_time
                if cur_time <= ftime:
                    edit_plan.start_time = utc_time
                if cur_time >= ftime:
                    delta = (cur_time - ftime).days
                    print "delta=", delta
                    total_tab1 = TotalTable.objects.filter(request_id=edit_plan.id)
                    print "len(total_tab1)", len(total_tab1)
                    print
                    total = 0
                    for i in range(delta + 1):
                        print "i=", i
                        itime = ftime + datetime.timedelta(days=i)
                        print itime
                        try:
                            curday = total_tab1.get(change_date=itime)
                            if curday.status == 'ongoing':
                                idaily_h = int(curday.daily_duration.split('H')[0])
                                idaily_p = int((curday.daily_duration.split('r')[1]).split('P')[0])
                                total = total + idaily_h * idaily_p
                        except:
                            print "not exist"
                            try:
                                lastday = total_tab1.get(change_date=(itime - datetime.timedelta(days=1)))
                                request_piece = edit_plan.request_duration.split('y')[1]
                                TotalTable.objects.create(change_date=itime,
                                                          daily_duration='24Hour' + request_piece,
                                                          status=lastday.status,
                                                          request_id=lastday.request_id)
                                curday = total_tab1.get(change_date=itime)
                                if curday.status == 'ongoing':
                                    request_p = int((edit_plan.request_duration.split('y')[1]).split('P')[0])
                                    total = total + 24 * request_p
                            except:
                                total = 0
                        print total
                else:
                    total = 0
                edit_plan.duration = total
                request_h = int(edit_plan.request_duration.split('H')[0])
                request_d = int((edit_plan.request_duration.split('r')[1]).split('D')[0])
                request_p = int((edit_plan.request_duration.split('y')[1]).split('P')[0])
                request_hours = request_h * request_d * request_p
                print "request_hours", request_hours
                if total >= request_hours:
                    edit_plan.isdelay = 'delay'
                elif 'delay' == edit_plan.isdelay:
                    edit_plan.isdelay = 'no'

                    #request_hour= int(edit_plan.request_duration.split('H')[0])
                    #request_day= int (edit_plan.request_duration.split)
                    #request_hours=request_hour+request_day*24
                    #real_duration = cur_time - dtime
                    #edit_plan.duration = real_duration
                    #real_days = real_duration.days
                    #real_seconds = real_duration.seconds
                    #real_hours =real_days * 24 + real_seconds / 3600
                    #print "request hours: %d" % request_hours
                    #print "real hours: %d" % real_hours
                    #if real_hours >= request_hours:
                        #edit_plan.status = 'delay'
                    #elif 'delay' == edit_plan.status:
                        #edit_plan.status = 'ongoing'
            
            print "test_closetime"
            close_time = request.POST['closeYearEdit']+"-"+request.POST['closeMonthEdit']+"-"+request.POST['closeDayEdit']+" "+request.POST['closeHourEdit']+":"+request.POST['closeMinuteEdit']+":"+request.POST['closeSecondEdit']
            if close_time != '-- ::':
                cltime = close_time.encode("utf-8")
                clotime = datetime.datetime.strptime(cltime, '%Y-%m-%d %H:%M:%S').date()
                cur_date = datetime.date.today()
                if clotime <= cur_date:
                    year = request.POST['closeYearEdit']
                    month = request.POST['closeMonthEdit']
                    day = request.POST['closeDayEdit']
                    hour = request.POST['closeHourEdit']
                    minute = request.POST['closeMinuteEdit']
                    second = request.POST['closeSecondEdit']
                    edit_ctime = year+"-"+month+"-"+day+" "+hour+":"+minute+":"+second
                    ctime = edit_ctime.encode("utf-8")
                    dtime = datetime.datetime.strptime(ctime,'%Y-%m-%d %H:%M:%S')
                    utc_time = dtime.replace(tzinfo=tz.gettz('CST'))
                    edit_plan.close_time = utc_time
                    edit_plan.status = 'close'

            print "next_target"
            next_target = request.POST['next_targetEdit']
            edit_plan.next_target = next_target

            edit_plan.save()
        elif 'delPlanId' in request.POST.keys():
            print "into delete plan"
            del_id = request.POST['delPlanId']
            del_plan = RequestTable.objects.get(id=del_id)
            del_plan.is_plan = 'false'
            del_plan.save()
        elif 'idEditCom' in request.POST.keys():
            print "into common user edit plan"
            edit_id = request.POST['idEditCom']
            edit_plan = RequestTable.objects.get(id=edit_id)
            edit_plan.progress = request.POST['progressEditCom']
            edit_plan.save()
        else:
            print "there is something wrong"
        #update plan table
        request_tab = RequestTable.objects.filter(is_plan="false")
        plan_tab = RequestTable.objects.filter(is_plan="true").order_by("id")
        print plan_tab
 
        for tab in plan_tab:
            tab.action_discription = tab.action_discription.replace("\n", "<br>")
            tab.progress = tab.progress.replace("\n", "<br>")
        return HttpResponseRedirect('/plan/', {"request_tab": request_tab, "plan_tab": plan_tab, 'valid_duration': valid_duration, 'valid_time':valid_time, 'valid_dailyDura':valid_dailyDura})
    else:
        for tab in plan_tab:
            stime = tab.start_time
            if stime and "close" != tab.status:
                stime = stime + datetime.timedelta(hours=8)
                ftimestr=stime.strftime('%Y-%m-%d %H:%M:%S')
                print "ftimestr=",ftimestr
                ftime1 = ftimestr.split(' ')[0]
                ftime = datetime.datetime.strptime(ftime1,'%Y-%m-%d').date()
                #ftime = datetime.datetime.strptime(stime.strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S').date()
                print "ftime=",ftime
                cur_time = datetime.date.today()
                #ctime = datetime.datetime.utcnow()
                #stime = datetime.datetime.strptime(stime.strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
                if cur_time >= ftime:
                    delta = (cur_time - ftime).days
                    print "delta=",delta
                    total_tab1 = TotalTable.objects.filter(request_id=tab.id)
                    print "len(total_tab1)",len(total_tab1)
                    print
                    total = 0
                    for i in range(delta+1):
                        print "i=",i
                        itime = ftime + datetime.timedelta(days=i)
                        print itime
                        try:
                            curday=total_tab1.get(change_date=itime)
                            if curday.status=='ongoing':
                                idaily_h = int(curday.daily_duration.split('H')[0])
                                idaily_p = int((curday.daily_duration.split('r')[1]).split('P')[0])
                                total = total + idaily_h * idaily_p
                        except:
                            print "not exist"
                            try:
                                lastday = total_tab1.get(change_date=(itime-datetime.timedelta(days=1)))
                                request_piece = tab.request_duration.split('y')[1]
                                TotalTable.objects.create(change_date=itime,
                                                      daily_duration='24Hour'+request_piece,
                                                      status=lastday.status,
                                                      request_id=lastday.request_id)
                                curday = total_tab1.get(change_date=itime)
                                if curday.status == 'ongoing':
                                    request_p = int((tab.request_duration.split('y')[1]).split('P')[0])
                                    total = total + 24 * request_p
                            except:
                                total = 0
                        print total
                else:
                    total = 0
                tab.duration = total
                request_h = int(tab.request_duration.split('H')[0])
                request_d = int((tab.request_duration.split('r')[1]).split('D')[0])
                request_p = int((tab.request_duration.split('y')[1]).split('P')[0])
                request_hours = request_h * request_d * request_p
                print "request_hours" , request_hours
                if total >= request_hours:
                    tab.isdelay = 'delay'
                elif 'delay' == tab.isdelay:
                    tab.isdelay = 'no'
                    #request_hours= int(tab.request_duration.split('H')[0])
                    #real_duration = ctime - stime
                    #tab.duration = real_duration
                    #real_days = real_duration.days
                    #real_seconds = real_duration.seconds
                    #real_hours =real_days * 24 + real_seconds / 3600
                    #print "request hours: %d" % request_hours
                    #print "real hours: %d" % real_hours
                    #if real_hours >= request_hours:
                        #tab.status = 'delay'
                    #elif 'delay' == tab.status:
                        #tab.status = 'ongoing'
                tab.save()
            tab.action_discription = tab.action_discription.replace("\n", "<br>")
            tab.progress = tab.progress.replace("\n", "<br>")
        return render(request, 'plan/plan.html', {"request_tab": request_tab, "plan_tab": plan_tab, 'valid_duration': valid_duration, 'valid_time':valid_time, 'valid_dailyDura':valid_dailyDura})