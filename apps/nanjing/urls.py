
from django.conf.urls import patterns, include, url 

import views

urlpatterns = patterns('',
    url(r'^(\w+)/articles-list/(\d+)/$', views.articles_list, name='articles_list'),
    url(r'^(\w+)/article-detail/(\d+)/$', views.article_detail, name='article_detail'),
    url(r'^(\w+)/open-account/$', views.open_account, name='open_account'),
    url(r'^(\w+)/sim-account/$', views.sim_account, name='sim_account'),
    url(r'^(\w+)/activity-user/(\d+)/$', views.activity_user, name='activity_user'),
    url(r'^(\w+)/commit-success/$', views.commit_success, name='commit_success'),
    url(r'^(\w+)/activity-list/$', views.activity_list, name='activity_list'),
    url(r'^(\w+)/show_question/$', views.show_question, name='show_question'),
)
