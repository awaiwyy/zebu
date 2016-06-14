#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import auth
from models import scheduleInfo
from models import projectInfo
import datetime
import os
from common import xlwt

# Create your views here.
schedule_file = "resources/tab/schedule_tab.xls"

def homePageData(request):
    schedule_item = []
    time1 = "10:00-22:00"
    time2 = "22:00-10:00"
    today = datetime.date.today()
    print today
    cur_month = today.month
    cur_week= today.isocalendar()
    print cur_week
    day = cur_week[2]
    next_monday = today + datetime.timedelta(days=8-day)
    next_month = next_monday.month
    next_week = next_monday.isocalendar()
    start_date = today - datetime.timedelta(days=day-1)
    end_date = today + datetime.timedelta(days=14-day)
       
    display_tab = scheduleInfo.objects.filter(sdate__gte = start_date, sdate__lte = end_date)
    project_tab = projectInfo.objects.filter(display="true")
    #if not os.path.exists(schedule_file):
        #saveScheduleTab(display_tab)

    #add or edit schedule table
    if request.method == 'POST' and "dateEdit0" in request.POST.keys():
        print "into edit schedule"
        for cnt in range(14):
            sdate = request.POST["dateEdit%d" % cnt]
            stime = request.POST["timeEdit%d" % cnt]
            total = request.POST["totalEdit%d" % cnt]
            used = request.POST["usedEdit%d" % cnt]
            arrangement = request.POST["arrangementEdit%d" % cnt]
            print [total, used, arrangement]
            if not total or not used or not arrangement:
                print "no compelete"
                continue
            '''
            if type(1) != type(total.strip()) or type(1) != type(used.strip()):
                print "total or used is wrong"
                continue
            '''
            if time1 == stime:
                stime = "daylight"
            else:
                stime = "night"
            try:
                try:
                    schedule_tab = scheduleInfo.objects.get(sdate=sdate, time=stime)
                    schedule_tab.total = total
                    schedule_tab.used = used
                    schedule_tab.arrangement = arrangement
                    schedule_tab.save()
                except:
                    print "not exist"
                    scheduleInfo.objects.create(sdate = sdate,
                                            time = stime,
                                            total = total,
                                            used = used,
                                            arrangement = arrangement)
            except ValueError:
                print "value type error"
                continue
            
        display_tab = scheduleInfo.objects.filter(sdate__gte = start_date, sdate__lte = end_date)
        #if not os.path.exists(schedule_file):
            #saveScheduleTab(display_tab)
        
    for i in range(14): #two week and twice one day
        date_item = start_date + datetime.timedelta(days=i/2)
        if i % 2 == 0:
            time_item = time1
        else:
            time_item = time2
        schedule_item.append([i, ' ', '', '', date_item, time_item])
    for tab in  display_tab:
        delta = (tab.sdate - start_date).days
        if delta > 6:
            if tab.time == 'daylight':
                delta_time =2 *delta + 14
            else:
                delta_time = 2 * delta + 15    
        else:
            if tab.time == "daylight":
                delta_time = 2 * delta
            else:
                delta_time = 2 * delta + 1
        #schedule_item[delta_time] = [delta_time, tab.total, tab.used, tab.arrangement, tab.sdate, tab.time]
        schedule_item[delta_time][1] = tab.total
        schedule_item[delta_time][2] = tab.used
        schedule_item[delta_time][3] = tab.arrangement

    cur_daylight = schedule_item[:14:2]
    cur_night = schedule_item[1:15:2]
    next_daylight = schedule_item[14::2]
    next_night = schedule_item[15::2]
    cur_date = []
    next_date = []
    for k in  range(7):
        cur_date.append(cur_daylight[k][4].day)
        #next_date.append(next_daylight[k][4].day)
        
    cur_date.append(cur_month)
    next_date.append(next_month)
        
    schedule_dict = {"schedule_tab": schedule_item, 
                     "curday_schedule": cur_daylight,
                    'curnight_schedule': cur_night,
                    "nextday_schedule": next_daylight,
                    'nextnight_schedule': next_night,
                    "cur_week": cur_week,
                    "next_week": next_week,
                    'cur_date': cur_date,
                    'next_date': next_date,
                    
        }
    return schedule_dict

def homeUser(request):
    print request.method
    print request.POST.keys()
    if request.method == 'POST' and 'userName' in request.POST.keys():
        print "into home post"
        #if 'userName' in request.POST.keys():
        #login to home
        print "login to home"
        username = request.POST['userName']
        password = request.POST['password']
        print "input0"
        print username
        print password
        user = auth.authenticate(username=username, password=password)
        print user
        if user is not None and user.is_active:
            auth.login(request, user)
            schedule_dict = homePageData(request)
            return HttpResponseRedirect('/home/', schedule_dict)
        else:
            #return render(request, 'login/login.html', {'password_is_wrong': True}) 
            return HttpResponse('Failed: username or password is error!')
    else:
        #other page(eg:request or plan page) to home 
        print "to home"
        schedule_dict = homePageData(request)   
        return render(request, 'home/home.html', schedule_dict)

def saveScheduleTab(schedule_tab):
    #set style
    font0 = xlwt.Font()
    font0.bold = True
    style0 = xlwt.XFStyle()
    style0.font = font0

    style = xlwt.XFStyle()
    style.num_format_str = 'YYYY-MM-DD'
    #creat sheet
    wb = xlwt.Workbook(encoding = 'utf-8')
    sheet = wb.add_sheet(u'schedule_tab', cell_overwrite_ok=True)

    row = 0  
    sheet.write(row, 0, 'Date', style0)
    sheet.write(row, 1, 'Time', style0)
    sheet.write(row, 2, 'Total', style0)
    sheet.write(row, 3, 'Used', style0)
    sheet.write(row, 4, 'Arrangement', style0)
    row += 1
    
    for tab in schedule_tab:
        sheet.write(row, 0, tab.sdate, style)
        if "daylight" == tab.time:
            show_time = "10:00-22:00"
        else:
            show_time = "22:00-10:00"
        sheet.write(row, 1, show_time)
        sheet.write(row, 2, tab.total)
        sheet.write(row, 3, tab.used)
        sheet.write(row, 4, tab.arrangement)
        row += 1
    wb.save(schedule_file)

def exportScheduleTab(request):
    schedule_tab = scheduleInfo.objects.all()
    saveScheduleTab(schedule_tab)
    
    file_name = schedule_file
    f = open(file_name)
    data = f.read()
    f.close()
 
    response = HttpResponse(data)   
    response['Content-Disposition'] = 'attachment; filename=%s' % file_name #show download frame
    return response
