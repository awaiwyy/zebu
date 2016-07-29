"""zebu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
import views as report_views

urlpatterns = [
    url(r'^$', report_views.report_Resource, name='resource_usage'),
    url(r'^daily_report$', report_views.reportPage, name='daily_report'),
    url(r'^resource_usage$',report_views.report_Resource,name='resource_usage'), 
    url(r'^main_tf_status$',report_views.report_MainTF,name='main_tf_status'), 
    url(r'^schedule$',report_views.report_Schedule,name='schedule'),
    url(r'^downloadfile/(.+)$', report_views.file_Download, name='downloadfile'),
    url(r'^ajaxget$',report_views.ajaxget,name='ajaxget'),
    url(r'^ajaxpost$',report_views.ajaxpost,name='ajaxpost$')
]