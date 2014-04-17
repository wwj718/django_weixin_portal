#!/usr/bin/env python2.7
#coding:utf8
import re
import hashlib

from django.shortcuts import render, render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404

from models import *

from yimi.settings import TOKEN

from utils import *

REPLY_DATA = '''
    <xml>
    <ToUserName><![CDATA[%s]]></ToUserName>
    <FromUserName><![CDATA[%s]]></FromUserName>
    <CreateTime>%s</CreateTime>
    <MsgType><![CDATA[%s]]></MsgType>
    %s
    </xml>
'''

TYPE_CONTENT_DICT = {
    'text': '<Content><![CDATA[%s]]></Content>',
    'news': '<ArticleCount>%s</ArticleCount><Articles>%s</Articles>'
}

ARTICLES = '''
    <item>
    <Title><![CDATA[%s]]></Title> 
    <Description><![CDATA[%s]]></Description>
    <PicUrl><![CDATA[%s]]></PicUrl>
    <Url><![CDATA[%s]]></Url>
    </item>
'''

def gen_xml(instance, app_item):
    retype = instance.message.retype
    type_content = TYPE_CONTENT_DICT.get(retype, '')
    resource = instance.message.get_resource()
   # user_info_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid='+app_item.appid+'&redirect_uri=%s&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect'
    #文本回复
    if retype == 'text':
        content = type_content % resource.content
        
        
    #    content = type_content % c

    #图文回复
    elif retype == 'news':
        if not resource:
            return ''
        articles_str = ''
        for article in resource.articles.all():
            art_param = (
                article.title, 
                article.description, 
                article.get_image_url(), 
                article.get_url(),
            )
            articles_str += ARTICLES % art_param
        content = type_content % (resource.articles.count(), articles_str)
    
    params = (
        instance.from_user,
        instance.to_user,
        instance.message.get_create_time(),
        retype,
        content,
    )
    return REPLY_DATA % params


def home(request):
    return render_to_response('home.html')

def index(request):
    '''网页授权获取用户基本信息'''
    api = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code'%(APPID, APP_SECRET, request.GET.get('code'))
    data = method_get_api(api)
    token = data.get('access_token')
    openid = data.get('openid')
    
    api2 = 'https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN'%(token, openid)
    print method_get_api(api2)
 
    return HttpResponse(json_data, content_type="application/json")


class ParseMessage():
    touser_re = r'<ToUserName><!\[CDATA\[(.+)\]\]></ToUserName>'
    fromuser_re = r'<FromUserName><!\[CDATA\[(.+)\]\]></FromUserName>'
    content_re = r'<Content><!\[CDATA\[(.+)\]\]></Content>'
    msgtype_re = r'<MsgType><!\[CDATA\[(.+)\]\]></MsgType>' 
    picurl_re = r'<PicUrl><!\[CDATA\[(.+)\]\]></PicUrl>'
    mediaid_re = r'<MediaId><!\[CDATA\[(.+)\]\]></MediaId>'
    msgid_re = r'<MsgId>(\d+)</MsgId>'        
    event_re = r'<Event><!\[CDATA\[(.+)\]\]></Event>'    
    eventkey_re = r'<EventKey><!\[CDATA\[(.+)\]\]></EventKey>'    
    latitude_re = r'<Latitude>(.+)</Latitude>'
    longitude_re = r'<Longitude>(.+)</Longitude>'
    precision = r'<Precision>(.+)</Precision>'

    def __init__(self, body, appitem):
        self.body = body
        self.appitem = appitem

    def parse_xml(self):     
        self.to_user = self.re_find(self.touser_re)
        self.from_user = self.re_find(self.fromuser_re)

        self.msgtype = self.re_find(self.msgtype_re)

        if self.msgtype != 'event':
            #关键字回复
            self.content = self.re_find(self.content_re)
            self.message = self.appitem.messages.filter(keyword=self.content, tag='keyword_recontent').first()  
            if not self.message:
                #无匹配回复
                self.message = self.appitem.messages.filter(tag='keyword_default_recontent').first()  
        else:
            self.event = self.re_find(self.event_re)
    
            if self.event == 'CLICK':
                #menu click事件
                self.eventkey = self.re_find(self.eventkey_re)
                self.message = self.appitem.messages.filter(tag='keyword_recontent', keyword=self.eventkey).first()
            elif self.event == 'subscribe':
                #关注,是否有EventKey，有的话，就是扫描带参数二维码事件
                self.message = self.appitem.messages.filter(tag=self.event).first() 
            elif self.event == 'unsubscribe':
                #取消关注
                pass
            elif self.event == 'LOCATION':
                #地理位置
                pass
            elif self.event == 'SCAN':
                # 扫描带参数二维码事件，用户已关注时的事件推送
                pass
            

    def re_find(self, re_str):
        data_result = re.findall(re_str, self.body)
        return data_result and data_result[0] or ''

    
def check(params):
    signature = params.get('signature', '')
    timestamp = params.get('timestamp', '')
    nonce = params.get('nonce', '')
    token = TOKEN

    tmp_str = ''.join(sorted([token, timestamp, nonce]))
    tmp_str = hashlib.sha1(tmp_str).hexdigest()
    if tmp_str == signature:
        return True
    else:
        return False        


@csrf_exempt
def weixin_api(request, slug):
    app_item = AppItem.objects.filter(id=slug).first()
    
    if not app_item or not check(request.GET):
        raise Http404
    
    #第一次验证开发者,如果失败，手动改is_valid为False,重新验证
    if not app_item.is_valid:
        echostr = request.GET.get('echostr', '')
        app_item.is_valid = True
        app_item.save()
        return HttpResponse(echostr)
    try:
        msg = ParseMessage(request.body, app_item)
        #file('/var/www/body.xml', 'w').write(request.body) #测试
        msg.parse_xml()
        return_data = ''
        if hasattr(msg, 'message'):
            if msg.message:
                return_data = gen_xml(msg, app_item)    
    except Exception, data:
        print '22222222222'
        print Exception, ":", data
    try:
        print 'aaaaaaaaaaa'
        if hasattr(msg, 'event'): 
            print 'bbbbbbbbbb'
            print msg.event
            #关注后增加用户信息
            if msg.event == 'subscribe':
                openid = msg.from_user
                user_info = app_item.get_user_info(openid)
                user = AppUser.objects.filter(openid=msg.from_user).first()
                if not user:
                    user = AppUser()
                user.nickname = user_info.get('nickname')
                user.openid = user_info.get('openid')
                user.sex = user_info.get('sex')
                user.language = user_info.get('language')
                user.city = user_info.get('city')
                user.province = user_info.get('province')
                user.country = user_info.get('country')
                user.headimgurl = user_info.get('headimgurl')
                user.save()
                if not app_item.app_users.filter(openid=openid).exists():
                    app_item.app_users.add(user)
            elif msg.event == 'unsubscribe':
                openid = msg.from_user
                user = AppUser.objects.filter(openid=openid).first()
                app_item.app_users.remove(user)
    except Exception,data:
        print Exception,":",data

    return HttpResponse(return_data, content_type="application/xhtml+xml")

def message(request):
    return HttpResponse('ok')

