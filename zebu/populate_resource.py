#!/usr/bin/env python
#coding:utf-8

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zebu.settings")

'''
Django 版本大于等于1.7的时候，需要加上下面两句
import django
django.setup()
否则会抛出错误 django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
'''

import django
if django.VERSION >= (1, 7):#自动判断版本
    django.setup()


def main():
    from apps.newhome.models import ResourceTable
    f = open('resource_list.txt','r')

    for line1 in f.readlines():
        line = line1.strip('\n')
        name,city,environment = line.split(',')
        # print '#####################'
        # print name,city,environment,len(city),len(environment)
        ResourceTable.objects.get_or_create(resource_id=name,city=city,environment=environment)

    f.close()

if __name__ == "__main__":
    main()
    print('Done!')