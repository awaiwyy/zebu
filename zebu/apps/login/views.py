#coding:utf-8
from django.shortcuts import render, render_to_response
from django.contrib import auth

# Create your views here.
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