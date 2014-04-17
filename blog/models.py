#coding:utf8

#import pytz
import time
import datetime
import urllib2
import os

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, m2m_changed
from django.core.cache import cache
from utils import upload_file_handler, method_get_api, method_post_api
from yimi.settings import TIME_ZONE, TOKEN_CACHE_PRE, TOKEN

TYPE_LIST = (
    ('text', '文本回复'),
    ('news', '图文回复'),
    ('event', 'event'),
)
RE_TYPE_LIST = (
    ('text', '文本回复'),
    ('news', '图文回复'),
)

MESSAGE_TAG = (
    ('keyword_recontent', '关键字回复'),
    ('keyword_default_recontent', '无匹配回复'),
    ('subscribe', '关注'),
   # ('unsubscribe', '取消订阅')
)

MENU_BUTTON_CHOICES = (
    ('click', '关键字回复'),
    ('view', '跳转'),
    ('sub_button', '子按键'),
)

SUB_BUTTON_CHOICES = (
    ('click', '单击动作'),
    ('view', '跳转'),
)

class Message(models.Model):
    type = models.CharField(max_length=100, blank=True, null=True, verbose_name='收到信息类型', choices=TYPE_LIST)
    keyword = models.CharField(max_length=100, blank=True, null=True, verbose_name='关键字')
    tag = models.CharField(max_length=100, default='keyword_recontent',verbose_name='标示', choices=MESSAGE_TAG)
    retype = models.CharField(max_length=100, verbose_name='返回信息类型', default='text',choices=RE_TYPE_LIST)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    class Meta:
        ordering = ['-id']
    def __unicode__(self):
        return '%s__%s' % (self.keyword or 'default', self.tag)

    def get_resource(self):
        if self.retype == 'text':
            return self.text_set.first()        
        elif self.retype == 'news':
            return self.news_set.first()
    def get_create_time(self):
     #   c_time = self.create_time
     #   to_zone = pytz.timezone(TIME_ZONE)
     #   local = c_time.astimezone(to_zone)
     #   return local.strftime("%Y%m%d%H%M")
        time_stamp=time.mktime(self.create_time.timetuple())
        return long(time_stamp)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u"Message"

class Text(models.Model):
    message = models.ForeignKey('Message', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="信息")
    content = models.TextField(blank=True, null=True, verbose_name='内容')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    def __unicode__(self):
        return self.content

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u"Text"

class News(models.Model):
    messages = models.ManyToManyField('Message', blank=True, null=True, verbose_name="信息")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    articles = models.ManyToManyField('Article', blank=True, null=True, verbose_name='素材') 
    order_dic = models.CharField(max_length=512, blank=True, null=True, verbose_name='素材顺序') #"{art1.id:1, art2.id:2}"
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = u"News"



class Article(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name='标题')
    author = models.CharField(max_length=100, blank=True, null=True, verbose_name='作者')
    description = models.TextField(blank=True, null=True, verbose_name='描述')
    picurl = models.CharField(max_length=500, blank=True, null=True, verbose_name='图片链接')
    url = models.CharField(max_length=500, blank=True, null=True, verbose_name='原文链接')
    image = models.FileField(
        max_length=128, blank=True, null=True, upload_to=upload_file_handler, verbose_name="本地上传")
    content = models.TextField(blank=True, null=True, verbose_name='正文')
    create_time = models.DateTimeField(auto_now_add=True,  blank=True, null=True,verbose_name='创建时间')
    class Meta:
        verbose_name_plural=verbose_name = '素材'

        ordering = ['-id']

    def __unicode__(self):
        return self.title
    def get_appitem(self):
            return self.appitem_set.first()

    def get_image_url(self):
        if self.picurl:
            return self.picurl
        elif self.image:
            appitem = self.get_appitem()
            domain = appitem.domain
            url_prefix = 'http://%s/media/' % domain
            return url_prefix + self.image.name
        else:
            return '/'
    
    def get_url(self):
        appitem = self.get_appitem()

        return 'http://%s/a/%s/article-detail/%s/' % (appitem.domain, appitem.slug, self.id)

    def get_description(self):
        if self.description:
            return self.description
        else:
            return self.content[:15]

    def get_category(self):
        return self.category_set.first()

class Category(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='名称')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    articles = models.ManyToManyField('Article', blank=True, null=True, verbose_name='素材') 
    status = models.BooleanField(default=True, verbose_name="是否显示")
    class Meta:
        ordering = ['-id']
    def __unicode__(self):
        return self.name
    
    def get_url(self):
        appitem = self.appitem_set.first()
        user_info_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid='+appitem.appid+'&redirect_uri=%s&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect'
        url = 'http://%s/a/%s/articles-list/%s/' % (appitem.domain, appitem.slug, self.id)
        return user_info_url % url
        return url

    class Meta:
        verbose_name_plural=verbose_name = 'Category'

#SUBSCRIBE_STATUS_CHOICES = (
#    (0, '未关注'),
#    (1, '关注'),
#)

class AppUser(models.Model):
   # subscribe = models.IntegerField(max_length=2, verbose_name="是否关注", blank=True, null=True, choices=SUBSCRIBE_STATUS_CHOICES)
    openid = models.CharField(max_length=128, blank=True, null=True, verbose_name='用户标识')
    nickname = models.CharField(max_length=128, blank=True, null=True, verbose_name='昵称')
    sex = models.IntegerField(max_length=2, verbose_name="性别", blank=True, null=True)
    city = models.CharField(max_length=128, blank=True, null=True, verbose_name='城市')
    province = models.CharField(max_length=128, blank=True, null=True, verbose_name='省份')
    country = models.CharField(max_length=128, blank=True, null=True, verbose_name='国家')
    language = models.CharField(max_length=128, blank=True, null=True, verbose_name='用户语言')
    headimgurl = models.CharField(max_length=500, blank=True, null=True, verbose_name='头像')
   # subscribe_time = models.CharField(max_length=20, blank=True, null=True, verbose_name='用户关注的时间')

    def __unicode__(self):
        return self.nickname

    class Meta:
        verbose_name_plural=verbose_name = 'AppUser'

class AppGroup(models.Model):
    groupid = models.CharField(max_length=128, blank=True, null=True, verbose_name='组id')
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='组名称')
    count = models.IntegerField(verbose_name="组内用户数量", default=0)
    app_users = models.ManyToManyField('AppUser', blank=True, null=True, verbose_name='组成员') 
    status = models.BooleanField(default=False, verbose_name="是否白名单组（可看到未显示的文章分类）")

    class Meta:
        verbose_name_plural=verbose_name = 'AppGroup'
        
class AppItem(models.Model):
    user = models.ForeignKey(User, verbose_name='用户', blank=True, null=True)
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='名称')
    slug = models.CharField(max_length=128, blank=True, null=True, verbose_name='app名称,唯一' )
    domain = models.CharField(max_length=128, blank=True, null=True, verbose_name='全域名(不包含http://)')
    appid = models.CharField(max_length=128, blank=True, null=True, verbose_name='APPID')
    app_secret = models.CharField(max_length=128, blank=True, null=True, verbose_name='APP_SECRET')
    token_cache_key = models.CharField(max_length=128, default='yimi_access_token', blank=True, null=True, verbose_name='缓存token的key')
    app_groups = models.ManyToManyField('AppGroup', blank=True, null=True, verbose_name='app内的组') 
    app_users = models.ManyToManyField('AppUser', blank=True, null=True, verbose_name='app内用户') 
    menu_buttons = models.ManyToManyField('MenuButton', blank=True, null=True, verbose_name='app内的button') 
    messages = models.ManyToManyField('Message', blank=True, null=True, verbose_name='app内的处理事件') 
    qrcodes = models.ManyToManyField('QRCode', blank=True, null=True, verbose_name='app内的二维码') 
    categories = models.ManyToManyField('Category', blank=True, null=True, verbose_name='分类') 
    articles = models.ManyToManyField('Article', blank=True, null=True, verbose_name='元素材') 
    news = models.ManyToManyField('News', blank=True, null=True, verbose_name='图文素材') 
    is_valid = models.BooleanField(default=False, verbose_name="是否验证")
    def __unicode__(self):
        return self.name or self.appid

    def get_weixin_api(self):
        return 'http://%s/%s/%s/' % (self.domain, TOKEN, self.id)
        
    def successed(self, data):
        if data.get('errcode') == 0 and data.get('errmsg') == 'ok':
            return True
        else:
            return False

    def get_token(self):
        token_cache_key = TOKEN_CACHE_PRE+'__'+self.appid #对不同的app指定不同的缓存
        token = cache.get(token_cache_key)
        if token:
            return token
        else:
            url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (self.appid, self.app_secret)
            dict_data = method_get_api(url)
            token = dict_data.get('access_token')
            expires_in = dict_data.get('expires_in')
            if token and expires_in:
                cache.set(token_cache_key, token, expires_in-60)
            return token or ''
    
    def get_all_user(self, next_id=None):
        '''得到所有用户列表''' 
        suffix = ''
        if next_id:
            suffix = '&next_openid=' + next_id
        return method_get_api('https://api.weixin.qq.com/cgi-bin/user/get?access_token='+self.get_token()+suffix)
    
    def get_user_info(self, openid):
        '''得到用户的详细信息''' 
        url = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN' % (self.get_token(), openid)
        return method_get_api(url)
    
    
    def create_menu(self, post_data):
        '''创建菜单，成功返回True'''
        url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token='+self.get_token()
        return_data = method_post_api(url, post_data)
        print return_data
        return self.successed(return_data)
    
    def select_menu(self):
        '''查询menu'''
        url = 'https://api.weixin.qq.com/cgi-bin/menu/get?access_token=' + self.get_token()
        return method_get_api(url)

    def delete_menu(self):
        '''删除menu'''
        url = 'https://api.weixin.qq.com/cgi-bin/menu/delete?access_token='+self.get_token()
        return self.successed(method_get_api(url))

    def create_qrcode(self, scene_id, permanent=False, expire_seconds=1800):
        '''创建带参数二维码,永久的要permanent=True'''
        scene_id = str(scene_id)
        url = 'https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token=%s' % self.get_token()
        if permanent:
            post_data = {"action_name": "QR_LIMIT_SCENE", "action_info": {"scene": {"scene_id": scene_id}}}
            dirpath = '/var/data/yimi-img/upload/qrcode/'+self.appid+'/permanent/'
            expire_seconds = 0
        else:
            post_data = {"expire_seconds": expire_seconds, "action_name": "QR_SCENE", "action_info": {"scene": {"scene_id": scene_id}}}
            dirpath = '/var/data/yimi-img/upload/qrcode/'+self.appid+'/tmp/'

        return_data = method_post_api(url, post_data)
        if return_data.get('ticket'):
            qrcode = self.qrcodes.filter(scene_id=scene_id).first()
            url = dirpath+scene_id+'.jpg'
            url = url.replace('/var/data/yimi-img/upload/', 'http://%s/media/' % self.domain)
            if not qrcode:
                qrcode = self.qrcodes.create(scene_id=scene_id, url=url, expire_seconds=expire_seconds)
            else:
                qrcode.url=url
                qrcode.expire_seconds=expire_seconds
                qrcode.save()
            filedata = urllib2.urlopen('https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket='+return_data.get('ticket')).read()
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)
            file(dirpath+scene_id+'.jpg', 'wb').write(filedata)
            
    def send_create_menu(self):
        '''发送创建menu''' 
        menu_buttons = self.menu_buttons.exclude(name=None).exclude(name="")
        button_data = []
        for button in menu_buttons:
            button_name = button.name
            if button.type == 'click':
                data = {
                    'type': 'click',
                    'name': button_name,
                    'key': button.key
                }
            elif button.type == 'view':
                data = {
                    'type': 'view',
                    'name': button_name,
                    'url': button.url,
                }
    
            elif button.type == 'sub_button':
                sub_data = []
                
                for sub_button in button.sub_button.exclude(name=None).exclude(name="") :
                    sub_button_name = sub_button.name
                    if sub_button.type == 'click':
                        son_data = {
                            'type': 'click',
                            'name': sub_button_name,
                            'key': sub_button.key
                        }
                    elif sub_button.type == 'view':
                        son_data = {
                            'type': 'view',
                            'name': sub_button_name,
                            'url': sub_button.url,
                        }
                    sub_data.append(son_data)
                data = {
                    'name': button.name,
                    'sub_button': sub_data
                }
            button_data.append(data)
        post_data = {'button':button_data}
        return self.create_menu(post_data)



    def get_user_openid(self, request):
        '''微网站获取用户openid'''
        code = request.GET.get("code", '')
        url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (self.appid, self.app_secret, code)
        data = method_get_api(url)
        openid = data.get("openid")
        return openid 

            
class QRCode(models.Model):
    scene_id = models.CharField(max_length=100, default='keyword_recontent',verbose_name='scene_id')        
    url = models.CharField(max_length=500, blank=True, null=True, verbose_name='资源链接')
    #permanent = models.BooleanField(default=False, verbose_name="是否永久有效")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    expire_seconds = models.IntegerField(verbose_name="过期时间", default=0, blank=True, null=True) #0时永久有效
    message = models.ForeignKey('Message', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="处理事件")

class MenuButton(models.Model):
    type = models.CharField(max_length=100, default='click',verbose_name='标示', choices=MENU_BUTTON_CHOICES)
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='名称')
    key = models.CharField(max_length=128, blank=True, null=True, verbose_name='关键字')
    url = models.CharField(max_length=500, blank=True, null=True, verbose_name='跳转链接')
    sub_button = models.ManyToManyField('SubButton', blank=True, null=True, verbose_name='子按键')  
    def __unicode__(self):
        return self.name

    def get_message(self):
        if self.type != 'click':
            return 
        appitem = self.appitem_set.first()
        message = appitem.messages.filter(keyword=self.key, tag='keyword_recontent').first()
        return message


class SubButton(models.Model):
    type = models.CharField(max_length=100, default='click',verbose_name='标示', choices=SUB_BUTTON_CHOICES)
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='名称')
    key = models.CharField(max_length=128, blank=True, null=True, verbose_name='关键字')
    url = models.CharField(max_length=500, blank=True, null=True, verbose_name='跳转链接')

    def __unicode__(self):
        return self.name

    def get_message(self):
        if self.type != 'click':
            return 
        menu_button = self.menubutton_set.first()
        appitem = menu_button.appitem_set.first()
        message = appitem.messages.filter(keyword=self.key, tag='keyword_recontent').first()
        return message



class Activity(models.Model):
    title = models.CharField(
        max_length=512, blank=True,null=True,verbose_name="名称")
    a_time = models.CharField(
        max_length=256, blank=True,null=True,verbose_name="时间")    
    xingshi = models.CharField(
        max_length=256, blank=True,null=True,verbose_name="形式")
    place = models.CharField(
        max_length=256, blank=True,null=True,verbose_name="地点")
    speaker = models.CharField(
        max_length=256, blank=True,null=True,verbose_name="主讲")
    count = models.IntegerField(verbose_name="人数", blank=True, null=True)
    appitem = models.ForeignKey(AppItem, verbose_name='应用', blank=True, null=True)
    content = models.TextField(blank=True, null=True, verbose_name='内容')
    activity_users = models.ManyToManyField('ActivityUser', verbose_name='参与人', blank=True, null=True)
    status = models.BooleanField(default=False, verbose_name="是否显示")
    class Meta:
        ordering = ['-id']

class ActivityUser(models.Model):
    name = models.CharField(
        max_length=128, blank=True,null=True,verbose_name="姓名")    
    cid = models.CharField(
        max_length=128, blank=True,null=True,verbose_name="身份证号")    
    tel = models.CharField(
        max_length=128, blank=True,null=True,verbose_name="电话")    
    lbs = models.CharField(
        max_length=256,  blank=True, verbose_name="位置")
    openid = models.CharField(
        max_length=256, blank=True, verbose_name="openid")
    create_time = models.DateTimeField(auto_now_add=True,  blank=True, null=True,verbose_name='创建时间')

class KeFu(models.Model):
    question = models.TextField(blank=True, null=True, verbose_name='提问')
    answer = models.TextField(blank=True, null=True, verbose_name='回答')
    create_time = models.DateTimeField(auto_now_add=True,  blank=True, null=True,verbose_name='创建时间')
    answer_time = models.DateTimeField(auto_now=True,  blank=True, null=True,verbose_name='回答时间')
    appuser = models.ForeignKey('AppUser', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="提问人")
    appitem = models.ForeignKey('AppItem', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="appitem")
    class Meta:
        ordering = ['-id']
    def __unicode__(self):
        return self.question or str(self.id)

#class Answer(models.Model):
#    content = models.TextField(blank=True, null=True, verbose_name='内容')
#    create_time = models.DateTimeField(auto_now_add=True,  blank=True, null=True,verbose_name='创建时间')
#    appuser = models.ForeignKey('AppUser', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="提问人")
#    appitem = models.ForeignKey('AppItem', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="appitem")
#    question = models.ForeignKey('Question', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="问题")
#
#    class Meta:
#        ordering = ['-id']
#    def __unicode__(self):
#        return self.content or ''

def send_create_menu(app_item):
    '''发送创建menu''' 
    menu_buttons = app_item.menu_buttons.all()
    button_data = []
    for button in menu_buttons:
        if button.type == 'click':
            data = {
                'type': 'click',
                'name': button.name,
                'key': button.key
            }
        elif button.type == 'view':
            data = {
                'type': 'view',
                'name': button.name,
                'url': button.url,
            }

        elif button.type == 'sub_button':
            sub_data = []
            
            for sub_button in button.sub_button.all():
                if sub_button.type == 'click':
                    son_data = {
                        'type': 'click',
                        'name': sub_button.name,
                        'key': sub_button.key
                    }
                elif sub_button.type == 'view':
                    son_data = {
                        'type': 'view',
                        'name': sub_button.name,
                        'url': sub_button.url,
                    }
                sub_data.append(son_data)
            data = {
                'name': button.name,
                'sub_button': sub_data
            } 
        button_data.append(data)
    post_data = {'button':button_data}
    app_item.create_menu(post_data)
    
#def menu_change_button(sender, instance, created, **kwargs):
#    '''menu_button保存发送更改菜单'''
#    app_item = instance.appitem_set.first()
#    if app_item:
#        send_create_menu(app_item)
#
def app_item_change_button(sender, instance, action, **kwargs):
    '''app_item的m2m字段变化，发送更改菜单'''
    send_create_menu(instance)

def app_item_saved(sender, instance, created, **kwargs):
    '''app_item保存发送更改菜单'''
    send_create_menu(instance)

#因为post_save()之后才调用m2m的变化，所以m2m信号也要加上
#m2m_changed.connect(app_item_change_button, sender=AppItem.menu_buttons.through)
#post_save.connect(menu_change_button, sender=MenuButton)
#post_save.connect(app_item_saved, sender=AppItem)

