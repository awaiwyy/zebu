#coding:utf-8
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.contrib import auth
from models import scheduleInfo
from models import projectInfo
import datetime
import os
from common import xlwt
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Create your views here.
temp_dir = os.path.join(BASE_DIR, "resources/tab/")
# Create your views here.
#temp_dir = "resources/tab/"
schedule_file = "schedule_tab.xls"


def homePageData(request,project_tab):
    #gopage = request.GET.get('page')
    schedule_item = []
    #time1 = "10:00-22:00"
    #time2 = "22:00-10:00"
    time = "0:00-24:00"
    today = datetime.date.today()
    print today
    cur_month = today.month
    cur_week= today.isocalendar()
    print cur_week
    day = cur_week[2]
    #next_monday = today + datetime.timedelta(days=8-day)
    #next_month = next_monday.month
    #next_week = next_monday.isocalendar()
    start_date = today - datetime.timedelta(days=day-1)
    end_date = today + datetime.timedelta(days=7-day)
       
    #display_tab = scheduleInfo.objects.filter(project_id=project_id ,sdate__gte = start_date, sdate__lte = end_date)

    #project_tab = projectInfo.objects.filter(display="true")
    #if not os.path.exists(schedule_file):
        #saveScheduleTab(display_tab)

    #add or edit schedule table
    if request.method == 'POST' and "dateEdit0" in request.POST.keys():
        print "into edit schedule"
        project_id = request.POST["project_idEdit"]
        print "project_id= ", project_id
        for cnt in range(7):
            sdate = request.POST["dateEdit%d" % cnt]
            stime = request.POST["timeEdit%d" % cnt]
            total = request.POST["totalEdit%d" % cnt]
            used = request.POST["usedEdit%d" % cnt]
            arrangement = request.POST["arrangementEdit%d" % cnt]
            # print [total, used, arrangement]
            if not total or not used :
                print "no compelete"
                continue
            '''
            if type(1) != type(total.strip()) or type(1) != type(used.strip()):
                print "total or used is wrong"
                continue
            '''
            if time == stime:
                stime = "oneday"
                #stime = "daylight"
            #else:
                #stime = "night"

            try:
                try:
                    schedule_tab = scheduleInfo.objects.filter(project_id=project_id).get(sdate=sdate)
                    schedule_tab.total = total
                    schedule_tab.used = used
                    schedule_tab.arrangement = arrangement
                    #schedule_tab.project_id = project_id
                    schedule_tab.save()
                except:
                    print "not exist"
                    scheduleInfo.objects.create(sdate = sdate,
                                            time = stime,
                                            total = total,
                                            used = used,
                                            arrangement = arrangement,
                                            project_id=project_id)
            except ValueError:
                print "value type error"
                continue
            
        #display_tab = scheduleInfo.objects.filter(sdate__gte = start_date, sdate__lte = end_date)
        #if not os.path.exists(schedule_file):
            #saveScheduleTab(display_tab)

    schedule_list = []
    cur_date = []
    for i in range(7):
        date_item = start_date + datetime.timedelta(days=i)
        cur_date.append(date_item.day)
    cur_date.append(cur_month)

    for project in project_tab:
        print "project.id: ",project.id
        display_tab = scheduleInfo.objects.filter(project_id = project.id, sdate__gte=start_date, sdate__lte=end_date)
        schedule_item =[]
        for i in range(7): #two week and twice one day
            #date_item = start_date + datetime.timedelta(days=i/2)
            date_item = start_date + datetime.timedelta(days=i)
            #if i % 2 == 0:
                #time_item = time1
            #else:
                #time_item = time2
            time_item = time
            schedule_item.append([i, ' ', '', '', date_item, time_item,''])
        for tab in  display_tab:
            delta = (tab.sdate - start_date).days
            #if delta > 6:
                #if tab.time == 'daylight':
                    #delta_time =2 *delta + 14
                #else:
                    #delta_time = 2 * delta + 15
            #else:
                #if tab.time == "daylight":
                    #delta_time = 2 * delta
                #else:
                    #delta_time = 2 * delta + 1
            #schedule_item[delta_time] = [delta_time, tab.total, tab.used, tab.arrangement, tab.sdate, tab.time]
            schedule_item[delta][1] = tab.total
            schedule_item[delta][2] = tab.used
            schedule_item[delta][3] = tab.arrangement
            schedule_item[delta][6] = project.id
            # schedule_item[delta][7] = project.project
            # schedule_item[delta][8] = project.spm
            # schedule_item[delta][9] = project.zebu
            print "total, used, arranage, project_id:",tab.total,tab.used,tab.arrangement,tab.project_id

        schedule_list.append({'pro':project,'sch':schedule_item})
        print "len(schedule_list)" ,len(schedule_list)
        for pro_i in schedule_list:
            print "pro_i['pro']",pro_i['pro'].id,pro_i['pro'].spm
            for i in range(7):
                print i, pro_i['sch'][i][0],pro_i['sch'][i][1], pro_i['sch'][i][2],pro_i['sch'][i][3], pro_i['sch'][i][6]

        #cur_daylight = schedule_item[:14:2]
        #cur_night = schedule_item[1:15:2]
    #cur_day = schedule_list[0]["sch"][:7:1]
        #next_daylight = schedule_item[14::2]
        #next_night = schedule_item[15::2]
    #cur_date = []
        #next_date = []
    # for k in  range(7):
    #     cur_date.append(cur_day[k][4].day)
            #next_date.append(next_daylight[k][4].day)

    #cur_date.append(cur_month)
        #next_date.append(next_month)
    # i=0
    # for pro_i in schedule_list:
    #     i =i+1
    #     for j in range(7):
    #         print i,pro_i['sch'][j][3],pro_i['sch'][j][6]

    #end for project in project_tab

    #Pagination -CC
    # perpage = 2 #show how many items per page
    
    # objects = schedule_list
    # pager = Paginator(objects,perpage)
    
    # try:
    #     projects = pager.page(gopage)

    # except PageNotAnInteger:
    #     projects = pager.page(1)
    # except EmptyPage:
    #     projects = pager.page(pager.num_pages)

    schedule_dict = {"schedule_tab": schedule_list,
                     "curday_schedule": schedule_list,
                    "cur_week": cur_week,
                    'cur_date': cur_date,
        }
    return schedule_dict

def homeUser(request):
    print request.method
    print request.POST.keys()
    project_tab = projectInfo.objects.filter(display="true").order_by("id")
    productlist=["iwhale2","isharkl2","Other"]
    for tab in project_tab:
        if tab.project in productlist:
            productlist.remove(tab.project)
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
            schedule_dict = homePageData(request,project_tab)
            schedule_dict.update(productlist=productlist)
            return HttpResponseRedirect('/home/', schedule_dict)
        else:
            #return render(request, 'login/login.html', {'password_is_wrong': True}) 
            return HttpResponse('Failed: username or password is error!')
    elif request.method == 'POST' and "projectInfo" in request.POST.keys():
        print"into new home project "
        project = request.POST["projectInfo"]
        spm = request.POST["spmInfo"]
        zebu = request.POST["zebuInfo"]
        if zebu.isdigit():
            projectInfo.objects.create(project=project,
                                   spm=spm,
                                   zebu=zebu)
        schedule_dict = homePageData(request,project_tab)
        schedule_dict.update(project_tab=project_tab)
        schedule_dict.update(productlist=productlist)
        return HttpResponseRedirect('/home/', schedule_dict)
    elif request.method == 'POST' and "projectEdit" in request.POST.keys():
        print"edit home project "
        edit_id = request.POST['idEdit']
        edit_home = projectInfo.objects.get(id=edit_id)
        edit_home.project = request.POST["projectEdit"]
        edit_home.spm = request.POST["spmEdit"]
        edit_home.zebu = request.POST["zebuEdit"]
        if edit_home.zebu.isdigit():
            edit_home.save()
        schedule_dict = homePageData(request,project_tab)
        schedule_dict.update(project_tab=project_tab)
        schedule_dict.update(productlist=productlist)
        return HttpResponseRedirect('/home/', schedule_dict)
    elif request.method == 'POST' and "delhomeId" in request.POST.keys():
        print"delete home project "
        del_id = request.POST['delhomeId']
        del_home = projectInfo.objects.get(id=del_id)
        del_home.display = 'false'
        del_home.save()
        schedule_dict = homePageData(request,project_tab)
        schedule_dict.update(project_tab=project_tab)
        schedule_dict.update(productlist=productlist)
        return HttpResponseRedirect('/home/', schedule_dict)
    else:
        #other page(eg:request or plan page) to home 
        print "to home"
    schedule_dict = homePageData(request,project_tab)
    schedule_dict.update(project_tab = project_tab)
    schedule_dict.update(productlist=productlist)
    return render(request, 'home/home.html', schedule_dict)
        #return render(request, 'home/home.html', {'project_tab': project_tab})

def saveScheduleTab(file_name):
    #set style
    font0 = xlwt.Font()
    font0.bold = True
    style0 = xlwt.XFStyle()
    style0.font = font0

    style = xlwt.XFStyle()
    style.num_format_str = 'YYYY-MM-DD'
    #creat sheet
    wb = xlwt.Workbook(encoding = 'utf-8')

    project_list = projectInfo.objects.filter(display="true").order_by("id")
    for project in project_list:
        #print "project.project: ", project.project
        sheet = wb.add_sheet(project.project, cell_overwrite_ok=True)
        row = 0
        sheet.write(row, 0, 'Date', style0)
        sheet.write(row, 1, 'Time', style0)
        sheet.write(row, 2, 'Total', style0)
        sheet.write(row, 3, 'Used', style0)
        sheet.write(row, 4, 'Arrangement', style0)
        row += 1

        #schedule_tab = scheduleInfo.objects.filter(project_id=project.id)
        today = datetime.date.today()
        cur_week = today.isocalendar()
        day = cur_week[2]
        start_date = today - datetime.timedelta(days=day - 1)
        end_date = today + datetime.timedelta(days=7 - day)
        #print "start_date",start_date
        #print "end_date",end_date

        schedule_tab = scheduleInfo.objects.filter(project_id=project.id, sdate__gte=start_date, sdate__lte=end_date)
        for tab in schedule_tab:
            #print "tab.sdate", tab.sdate
            sheet.write(row, 0, tab.sdate, style)
            sheet.write(row, 1, tab.time)
            sheet.write(row, 2, tab.total)
            sheet.write(row, 3, tab.used)
            sheet.write(row, 4, tab.arrangement)
            row += 1
    wb.save(file_name)

def exportScheduleTab(request):
    #schedule_tab = scheduleInfo.objects.all()
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)

    file_name = temp_dir + schedule_file
    saveScheduleTab(file_name)
    
    f = open(file_name,"rb")
    data = f.read()
    f.close()
 
    response = HttpResponse(data)   
    response['Content-Disposition'] = 'attachment; filename=%s' % file_name #show download frame
    return response
