#coding:utf8

import datetime
import hashlib
import json
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

def generate_code(plainText):
    return hashlib.sha1(plainText).hexdigest()

def getnowString():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%s%f')

def generate_file_code():
    nowString = getnowString()
    key = "yimi_upload_file_%s" % nowString
    return generate_code(key)

def upload_file_handler(filename):
    suffix = filename.split(".")[-1] or "jpg"
    filename = generate_file_code()+"."+suffix
    return filename


@csrf_exempt
def upload(request):
    try:
        original = request.POST.get('fileName')
        filename = upload_file_handler(original)
        filepath = '/var/data/yimi-img/upload/ueditor/'+filename
        url = 'http://'+ request.get_host()+ '/media/ueditor/'+filename
        data = request.FILES.get('upfile').read()
        file(filepath, 'wb').write(data)
        re_data = { 
            'url': url,
            'title': filename,
            'original': original,
            'state': 'SUCCESS',
        }   
        js_data = json.dumps(re_data)
    except Exception, e:
        print Exception, ':', e
    return HttpResponse(js_data, content_type="application/xhtml+xml")
