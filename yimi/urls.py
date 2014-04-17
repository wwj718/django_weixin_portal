#coding:utf-8
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from yimi.settings import TOKEN
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^%s/(\d+)/$'%TOKEN, 'blog.views.weixin_api', name='weixin_api'),
    url(r'^$', 'blog.views.message', name='message'),
    url(r'^yimi-admin/', include('blog.urls', namespace="yimi_admin")),
    url(r'^a/', include('apps.nanjing.urls', namespace="nanjing")), #appitem slug

    url(r'^myueditor/upload/$', 'myueditor.views.upload', name='upload'),
    url(r'^admin/', include(admin.site.urls)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
