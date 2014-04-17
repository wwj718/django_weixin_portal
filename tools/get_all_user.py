#!/usr/bin/env python2.7
# -*- encoding:utf8 -*-
import sys
import os

os.environ['DJANGO_SETTINGS_MODULE'] = "yimi.settings"
sys.path.append("/var/www/sites/yimi")
from blog.models import AppItem, AppUser



if __name__ == '__main__':
    appitem = AppItem.objects.get(slug="xueersi")
    all_user = appitem.get_all_user()
    print all_user.get("total")
    print all_user.get("count")
    print all_user.get("data").get("openid")
    print all_user.get('next_openid')
    openid_list = all_user.get("data").get("openid")
    
    for openid in openid_list:
        print openid
        appuser = AppUser.objects.filter(openid=openid)
        print appuser
        if not appuser:
            print 'create!'
            appuser = AppUser.objects.create(openid=openid)
        
        else:
            appuser = appuser[0]
        if appuser not in appitem.app_users.all():
            print 'join in!'
            appitem.app_users.add(appuser)
        
