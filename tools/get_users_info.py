#!/usr/bin/env python2.7
#coding:utf8
import sys
import os

os.environ['DJANGO_SETTINGS_MODULE'] = "yimi.settings"
sys.path.append("/var/www/sites/yimi")
from blog.models import AppItem, AppUser



if __name__ == '__main__':
    appitem = AppItem.objects.get(slug='xueersi')
    
    users = appitem.app_users.all()
    for user in users:
        try:
            print 'now is ==', user.openid
            if user.language:
                continue
        
            data = appitem.get_user_info(openid=user.openid)
            user.nickname = data.get('nickname')
            user.sex = data.get('sex')
            user.language = data.get('language')
            user.city = data.get('city')
            user.province = data.get('province')
            user.country = data.get('country')
            user.headimgurl = data.get('headimgurl')
            user.save()
        except:
            print '!!!===', user.openid
