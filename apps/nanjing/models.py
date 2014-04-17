#coding:utf8

from django.db import models
from blog.utils import upload_file_handler
from blog.models import Article, AppItem
from django.contrib.auth.models import User

class OpenAccount(models.Model):
    appitem = models.ForeignKey(AppItem, verbose_name='应用', blank=True, null=True)
    name = models.CharField(
        max_length=128, blank=True,null=True,verbose_name="姓名")      
    cid = models.CharField(
        max_length=128, blank=True,null=True,verbose_name="身份证号")      
    tel = models.CharField(
        max_length=128, blank=True,null=True,verbose_name="电话")      
    images = models.ManyToManyField(
        "ImageItem", null=True, blank=True, verbose_name="图片")
    lbs = models.CharField(
        max_length=256, blank=True, verbose_name="位置")
    openid = models.CharField(
        max_length=256, blank=True, verbose_name="openid")
    create_time = models.DateTimeField(auto_now_add=True,  blank=True, null=True,verbose_name='创建时间')
    
class ImageItem(models.Model):
    name = models.CharField(
        max_length=128, blank=True,null=True,verbose_name="状态")      
    image = models.ImageField(
        max_length=128, upload_to=upload_file_handler, verbose_name="图片")


class SimAccount(models.Model):
    appitem = models.ForeignKey(AppItem, verbose_name='应用', blank=True, null=True)
    name = models.CharField(
        max_length=128, blank=True,null=True,verbose_name="姓名")      
    cid = models.CharField(
        max_length=128, blank=True,null=True,verbose_name="身份证号")      
    tel = models.CharField(
        max_length=128, blank=True,null=True,verbose_name="电话")      
    lbs = models.CharField(
        max_length=256, blank=True, verbose_name="位置")
    bank = models.CharField(
        max_length=256, blank=True, verbose_name="开户银行")
    openid = models.CharField(
        max_length=256, blank=True, verbose_name="openid")
    create_time = models.DateTimeField(auto_now_add=True,  blank=True, null=True, verbose_name='创建时间')

#class Activity(models.Model):
#    title = models.CharField(
#        max_length=512, blank=True,null=True,verbose_name="名称")      
#    a_time = models.CharField(
#        max_length=256, blank=True,null=True,verbose_name="时间")      
#    count = models.IntegerField(verbose_name="人数", blank=True, null=True)
#    appitem = models.ForeignKey(AppItem, verbose_name='应用', blank=True, null=True)
#    activity_users = models.ManyToManyField('ActivityUser', verbose_name='参与人', blank=True, null=True)
#
#class ActivityUser(models.Model):
#    name = models.CharField(
#        max_length=128, blank=True,null=True,verbose_name="姓名")      
#    cid = models.CharField(
#        max_length=128, blank=True,null=True,verbose_name="身份证号")      
#    tel = models.CharField(
#        max_length=128, blank=True,null=True,verbose_name="姓名")      
#    lbs = models.CharField(
#        max_length=256,  blank=True, verbose_name="位置")
#    openid = models.CharField(
#        max_length=256, blank=True, verbose_name="openid")
#    create_time = models.DateTimeField(auto_now_add=True,  blank=True, null=True,verbose_name='创建时间')
