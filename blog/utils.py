#coding:utf8
import datetime
import hashlib
import os
import urllib
import urllib2
import json

from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def generate_code(plainText):
    return hashlib.sha1(plainText).hexdigest()

def getnowString():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%s%f')

def generate_file_code():
    nowString = getnowString()
    key = "yimi_upload_file_%s" % nowString
    return generate_code(key)

def upload_file_handler(instance,filename):
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    path = date_str +"/"+instance.__class__.__name__.lower()
    suffix = filename.split(".")[-1] or "jpg"
    filename = generate_file_code()+"."+suffix
    return os.path.join(path, filename)

def method_get_api(url):
    response = urllib2.urlopen(url).read()
    dict_data = json.loads(response)
    return dict_data

def method_post_api(url, post_data):
    if post_data:
        json_data = json.dumps(post_data, ensure_ascii=False).encode('utf8')
    else:
        return ''
  #  json_data = json.dumps(post_data)
    print 'json_data==', json_data
    req = urllib2.Request(url, json_data)
    req.add_header('Context-Type', 'application/json;charset=utf-8')
    return_json = urllib2.urlopen(req).read()
    return json.loads(return_json)

def get_user_openid(appid, secret, code):
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (appid, secret, code)
    data = method_get_api(url)
    openid = data.get("openid")
    return openid 
def convert_get_data(GET, key_list):
    '''翻页时用来继承get提交参数'''
    get_data = ''
    for keyw in key_list:
        if GET.get(keyw):
            get_data += '%s=%s&'%(keyw, GET.get(keyw))
    return get_data

def get_entry_page(entry, count_per_page, page_number):
    '''分页返回page_number页的数据'''
    paginator = Paginator(entry, count_per_page)
    try:
        page_entry = paginator.page(page_number)
    except PageNotAnInteger:
        page_entry = paginator.page(1)
    except EmptyPage:
        page_entry = paginator.page(paginator.num_pages)
    return page_entry

def page_turning(list_obj, request, count=10):
    '''翻页函数''' 
    page = int(request.GET.get("p",1))
    matchs = get_entry_page(list_obj, count, page)
    show_pages = range(max(page-4,1),min(page+4,matchs.paginator.num_pages)+1)
    return (matchs, show_pages)


#successed(data):
#    if data.get('errcode') == 0 and data.get('errmsg') == 'ok':
#        return True
#    else:
#        return False
#
#def get_token():
#    token = cache.get(TOKEN_CACHE_KEY)
#    if token:
#        return token
#    else:
#        url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s' % (APPID, APP_SECRET)
#        dict_data = method_get_api(url)
#        token = dict_data.get('access_token')
#        expires_in = dict_data.get('expires_in')
#        if token and expires_in:
#            cache.set(TOKEN_CACHE_KEY, token, expires_in-60)
#        return token
#
#def operate_group(keyword, post_data=None):
#    token = get_token()
#    url = GROUP_API.get(keyword)+token
#    if not token:
#        return
#    if keyword == 'get_all_group':
#        return method_get_api(url)
#    else:
#        return method_post_api(url, post_data)
#
#def get_all_user(next_id=None):
#    '''得到所有用户列表'''
#    suffix = ''
#    if next_id:
#        suffix = '&next_openid=' + next_id
#    return method_get_api('https://api.weixin.qq.com/cgi-bin/user/get?access_token='+get_token()+suffix)
#
#def get_user_info(openid):
#    '''得到用户的详细信息'''
#    url = 'https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN' % (get_token(), openid)
#    return method_get_api(url)
#
#
#def create_menu(post_data):
#    '''创建菜单，成功返回True'''
#    url = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token='+get_token()
#    return_data = method_post_api(url, post_data)
#    return successed(return_data)
#       
#def select_menu():
#    '''查询menu'''
#    url = 'https://api.weixin.qq.com/cgi-bin/menu/get?access_token=' + get_token()
#    return method_get_api(url)
#
#def delete_menu():
#    '''删除menu'''
#    url = 'https://api.weixin.qq.com/cgi-bin/menu/delete?access_token='+get_token() 
#    return successed(method_get_api(url))
