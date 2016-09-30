#coding:utf-8
from django.shortcuts import render, render_to_response
from django.contrib import auth
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User,Group
from urlparse import urljoin
import requests
import json

# Create your views here.
bzurl = "http://bugzilla.spreadtrum.com/bugzilla/rest/"

def configure( bzurl, username, password):
    bzurl = bzurl
    if not bzurl.endswith("/"):
        bzurl += "/"
    username = username
    password = password
def request(method, path, username, password):
    url = urljoin(bzurl, path)
    if method in ("GET", "HEAD"):
        params = {"Bugzilla_login": username,"Bugzilla_password": password,}
    headers = { "Accept": "application/json","Content-Type": "application/json",}
    try:
        r = requests.request(method, url, params=params,headers=headers)
        r.raise_for_status()
    except requests.RequestException as e:
        print(e)
    return r.status_code
def loginBugzilla(username, password):
    return request("GET","login",username, password)

def login(request, **kwargs):
    #print "into login"
    '''
    response = render_to_response('login/login.html')
    # 在客户端Cookie中添加Post表单token，避免用户重复提交表单
    response.set_cookie("postToken",value='allow')
    return response
    '''
    return render(request, 'login/login.html')
    '''
    token = "allow" # 可以采用随机数
    request.session['postToken'] = token
    # 将Token值返回给前台模板
    return render_to_response('login/login.html',{'postToken':token})
    '''

def main(request, **kwargs):
    auth.logout(request)
    return render(request, 'login/index.html')


def userIntoZebuDB(zebuUser):
    email=zebuUser+"@spreadtrum.com"
    #将表单写入数据库
    user = User()
    user.username = zebuUser
    user.set_password(zebuUser) #更改密码，并自动处理hash值
    user.email = email
    user.save()

    com_group = Group.objects.get(name="com user")
    user.groups=[com_group]

def ajaxpost(request):
    if 'userName' in request.POST.keys():
        bugzilla_username = request.POST['userName']
        print "bugzilla_username", bugzilla_username
        bugzilla_password = request.POST['password']
        zebuUser = ""
        print "bugzilla_username",bugzilla_username
        try:
            user = User.objects.get(username=bugzilla_username)
            zebuUser = user.username
        except:
            print "该用户不存在zebu数据库"

        configure(bzurl, bugzilla_username, bugzilla_password)
        result = loginBugzilla(bugzilla_username, bugzilla_password)
        if result == 200:
            print "验证通过"
            print "verify is ok"
            if zebuUser == "":
                zebuUser = bugzilla_username.lower()
                userIntoZebuDB(zebuUser)
                print zebuUser
            # 用户登录zebu数据库，以使用用户权限管理系统
            zebuUser = zebuUser.lower()
            user = auth.authenticate(username=zebuUser, password=zebuUser)
            auth.login(request, user)
            result = "1"
        else:
            print "验证未通过,请修改用户名或密码"
            result = "0"
        success_dict = {"result": result}
        return HttpResponse(json.dumps(success_dict),content_type="application/json")