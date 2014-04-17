#coding:utf8
from django.conf.urls import patterns, include, url 

import myadmin

urlpatterns = patterns('',
    url(r'^$', myadmin.news_list, name='news_list'),
    url(r'^category-list/$', myadmin.category_list, name='category_list'),
    url(r'^news-add/$', myadmin.news_add, name='news_add'),  #news意义已失效，但仍有。此处是添加,修改文章
    url(r'^article-detail/(\d+)/$', myadmin.article_detail, name='article_detail'),
    url(r'^articles-list/$', myadmin.articles_list, name='articles_list'),
    #url(r'^article-update/$', myadmin.article_update, name='article_update'),
    url(r'^article-delete/(\d+)/$', myadmin.article_delete, name='article_delete'),
    url(r'^login/$', myadmin.mylogin, name='login'),
    url(r'^logout/$', myadmin.mylogout, name='logout'),

    url(r'^reply/$', myadmin.reply, name='reply'),  #关注回复，无匹配回复, 关键字编辑
    url(r'^message-update/$', myadmin.message_update, name='message_update'),  #message的所有修改
    url(r'^keyword-reply/$', myadmin.keyword_reply, name='keyword_reply'),
    url(r'^users-list/$', myadmin.users_list, name='users_list'),
    url(r'^groups-list/$', myadmin.groups_list, name='groups_list'),
    url(r'^groups-delete/$', myadmin.groups_delete, name='groups_delete'),
    url(r'^group-name-update/$', myadmin.group_name_update, name='group_name_update'),
    url(r'^category-delete/$', myadmin.category_delete, name='category_delete'),
    url(r'^category-name-update/$', myadmin.category_name_update, name='category_name_update'),
    url(r'^category-add/$', myadmin.category_add, name='category_add'),
    url(r'^category-remove/$', myadmin.category_remove, name='category_remove'),

    url(r'^menus-list/$', myadmin.menus_list, name='menus_list'),
    url(r'^send-create-menu/$', myadmin.send_create_menu, name='send_create_menu'),
    url(r'^menu-add/$', myadmin.menu_add, name='menu_add'),
    url(r'^menu-update/$', myadmin.menu_update, name='menu_update'),
    url(r'^menu-click/$', myadmin.menu_click, name='menu_click'),
    url(r'^menu-url/$', myadmin.menu_url, name='menu_url'),
    url(r'^menu-delete/$', myadmin.menu_delete, name='menu_delete'),
    url(r'^menu-change-name/$', myadmin.menu_change_name, name='menu_change_name'),
    url(r'^sub-menu-update/$', myadmin.sub_menu_update, name='sub_menu_update'),
    url(r'^sub-menu-add/$', myadmin.sub_menu_add, name='sub_menu_add'),

    url(r'^text-update/$', myadmin.text_update, name='text_update'),
    url(r'^news-update/$', myadmin.news_update, name='news_update'),
   # url(r'^keyword-update/(\d+)/$', myadmin.keyword_update, name='keyword_update'),
    url(r'^keyword-add/$', myadmin.keyword_add, name='keyword_add'),
    url(r'^keyword-delete/$', myadmin.keyword_delete, name='keyword_delete'),
    url(r'^groups-add/$', myadmin.groups_add, name='groups_add'),
    url(r'^group-update/$', myadmin.group_update, name='group_update'),
    url(r'^group-remove/$', myadmin.group_remove, name='group_remove'),

    url(r'^activity-list/$', myadmin.activity_list, name='activity_list'),
    url(r'^open-account-list/$', myadmin.open_account_list, name='open_account_list'),
    url(r'^sim-account-list/$', myadmin.sim_account_list, name='sim_account_list'),


    url(r'^account-delete/(\w+)/(\d+)/$', myadmin.account_delete, name='account_delete'),
    url(r'^activity-add/$', myadmin.activity_add, name='activity_add'),
    url(r'^activity-delete/(\d+)/$', myadmin.activity_delete, name='activity_delete'),
    url(r'^activity-account-list/(\d+)/$', myadmin.activity_account_list, name='activity_account_list'),
    url(r'^activity-status/(\d+)/$', myadmin.activity_status, name='activity_status'),


    url(r'^questions-list/$', myadmin.questions_list, name='questions_list'),  #客服列表
    url(r'^answer-question/$', myadmin.answer_question, name='answer_question'),  #客服列表
    url(r'^kefu-delete/$', myadmin.kefu_delete, name='kefu_delete'),  #客服列表

)
