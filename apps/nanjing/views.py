#coding:utf8
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from blog.models import *
from blog.utils import get_user_openid
from blog.utils import get_entry_page, page_turning
from models import *

def get_appitem(slug):
    appitem = AppItem.objects.filter(slug=slug).first()
    return appitem



def article_detail(request, slug, id):
    appitem = get_appitem(slug)
    article = Article.objects.filter(id=id).first()
    if not article:
        raise Http404
    context = { 
        'article': article,
        'appitem': appitem,
    }   
    return render_to_response('nanjing/article_detail.html', context,
        context_instance=RequestContext(request))

def articles_list(request, slug, id):
   # category = Category.objects.filter(id=id, status=True).first()
   # appitem = category.appitem_set.first()
    appitem = get_appitem(slug)
    code = request.GET.get("code", '')
   # openid = get_user_openid(appitem.appid, appitem.app_secret, code)
    openid = appitem.get_user_openid(request)
    category = appitem.categories.get(id=id)        
    if openid and code:
        user = AppUser.objects.get(openid=openid)
        if not category.status: #不显示的分类
            if appitem.app_groups.filter(app_users=user, status=True).exists():
                articles = category.articles.all()
            else:
                return render_to_response('nanjing/notavailable.html', {},
                    context_instance=RequestContext(request))
        else:
            articles = category.articles.all()
    elif not code:
        articles = category.articles.all()
    else:
        articles = []
            
    page = int(request.GET.get("p",1))
   # return_articles = get_entry_page(articles,10,page)
    matchs, show_pages = page_turning(articles, request, 4)
    context = { 
        'appitem': appitem,
        'articles': articles,
        'matchs': matchs,
    }   
    return render_to_response('nanjing/articles_list.html', context,
        context_instance=RequestContext(request))

def reverse_url(slug):
    return reverse("nanjing:commit_success", args=(slug,))

def open_account(request, slug):
    appitem = get_appitem(slug)
    if request.method == "POST":
        name = request.POST.get('name')
        cid = request.POST.get('cid')
        tel = request.POST.get('tel')
        openaccount = appitem.openaccount_set.filter(cid=cid).first()
        if not openaccount:
            appitem.openaccount_set.create(name=name, cid=cid, tel=tel)
            return HttpResponseRedirect(reverse_url(slug))
    context = {'appitem': appitem}
    
    return render_to_response('nanjing/open_account_form.html', context,
        context_instance=RequestContext(request))

def sim_account(request, slug):
    appitem = get_appitem(slug)
    if request.method == "POST":
        name = request.POST.get('name')
        cid = request.POST.get('cid')
        tel = request.POST.get('tel')
        bank = request.POST.get('bank')
        simaccount = appitem.simaccount_set.filter(cid=cid).first()
        if not simaccount:
            appitem.simaccount_set.create(name=name, cid=cid, tel=tel, bank=bank)
            return HttpResponseRedirect(reverse_url(slug))
    context = {'appitem': appitem}
    
    return render_to_response('nanjing/sim_account_form.html', context,
        context_instance=RequestContext(request))

def activity_user(request, slug, cid):
    appitem = get_appitem(slug)
    activity = appitem.activity_set.filter(id=cid).first()
    if request.method == "POST":
        name = request.POST.get('name')
        cid = request.POST.get('cid')
        tel = request.POST.get('tel')
       # openid = request.POST.get("openid")
       # if openid and activity.activity_users.filter(openid=openid).exists():
        activity.activity_users.create(name=name, cid=cid, tel=tel)
        return HttpResponseRedirect(reverse_url(slug))
    context = {'appitem': appitem, 'activity': activity}
    
    return render_to_response('nanjing/activity_user_form.html', context,
        context_instance=RequestContext(request))

def commit_success(request, slug):
    return render_to_response('nanjing/commit_success.html', {},
        context_instance=RequestContext(request))
def activity_list(request, slug):
    appitem = get_appitem(slug)
    activities = appitem.activity_set.filter(status=True)
    matchs, show_pages = page_turning(activities, request, 1)
    context = {'appitem': appitem, 'activities': activities, 'matchs': matchs}
    
    return render_to_response('nanjing/activity_list.html', context,
        context_instance=RequestContext(request))

def show_question(request, slug):
    '''客户服务'''
    appitem = get_appitem(slug)
    if request.method == 'POST':
        openid = request.POST.get('openid')
        question = request.POST.get('question')
        if openid:
            user = AppUser.objects.filter(openid=openid).first()
            if not user:
                user = AppUser.objects.create(openid=openid)
            KeFu.objects.create(appitem=appitem, appuser=user, question=question)
            return HttpResponseRedirect(reverse_url(slug))

    openid = appitem.get_user_openid(request)
    kefus = None
    if openid:
        user = AppUser.objects.filter(openid=openid).first()
        if not user:
            user = AppUser.objects.create(openid=openid)
        kefus = KeFu.objects.filter(appitem=appitem, appuser=user)
    context = {
        'kefus': kefus,
        'openid': openid,
        'appitem': appitem,
    }
    return render_to_response('nanjing/show_question.html', context,
        context_instance=RequestContext(request))

