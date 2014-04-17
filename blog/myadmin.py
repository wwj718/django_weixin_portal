#coding:utf8

import json
import re

from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse

from utils import convert_get_data, get_entry_page
from models import *
from yimi_forms import *

LOGIN_URL = '/yimi-admin/login/'

def mylogout(request):
    logout(request)
    return HttpResponseRedirect(LOGIN_URL)

def mylogin(request):
    logout(request)
    next = request.GET.get("next")
    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        next = request.POST.get("next")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            if next:
                return HttpResponseRedirect(next)
            return HttpResponseRedirect(reverse("yimi_admin:news_list"))
    return render_to_response('yimi_admin/login.html', {"next": next},
        context_instance=RequestContext(request))
def get_appitem(user):
    if user:
        return AppItem.objects.filter(user=user).first()

def page_turning(list_obj, request, count=10):
    '''翻页函数'''

    page = int(request.GET.get("p",1))
    matchs = get_entry_page(list_obj, count, page)
    show_pages = range(max(page-4,1),min(page+4,matchs.paginator.num_pages)+1)
    return (matchs, show_pages)


@login_required(login_url=LOGIN_URL)
def news_list(request):
    appitem = get_appitem(request.user)
    articles = appitem.articles.all()
    
    matchs, show_pages = page_turning(articles, request, 10)
    context = {
        'articles': articles,
        'matchs': matchs,
        'show_pages': show_pages,
    }
    return render_to_response('yimi_admin/news_list.html', context,
        context_instance=RequestContext(request))

@login_required(login_url=LOGIN_URL)
def category_list(request):
    appitem = get_appitem(request.user)
    categories = appitem.categories.all()
    yisi = False
    if appitem.categories.filter(status=False).exists():
        yisi = True
    context = {
        'categories': categories,
        'appitem': appitem,
        'yisi': yisi,
    }
    return render_to_response('yimi_admin/category_list.html', context,
        context_instance=RequestContext(request))

    
@login_required(login_url=LOGIN_URL)
def news_add(request):
    '''发表文章,实际为article_add'''
    appitem = get_appitem(request.user)
    #news_id = request.GET.get('news_id')
   # if news_id:
    #    news = appitem.news.get(id=news_id)
   # else:
   #     news = appitem.news.create()
    article_id = request.GET.get("article")
    if article_id:
        article = appitem.articles.get(id=article_id)
        out_categories = appitem.categories.exclude(articles=article)
        in_categories = appitem.categories.filter(articles=article)
    else:
        article = None
        out_categories = appitem.categories.all()
        in_categories = None
    if request.method == 'POST':
        postdata = request.POST
        if article:
            print 'cccccccccccc'
            articleform = ArticleForm(request.POST, request.FILES, instance=article)
        else:
            articleform = ArticleForm(request.POST, request.FILES)
        if articleform.is_valid():
            article = articleform.save()
            category_name = postdata.get('category').strip()
            if category_name:
                category = appitem.categories.filter(name=category_name).first()
                if not category:
                    category = appitem.categories.create(name=category_name)
                if not category.articles.filter(id=article.id).exists():
                    category.articles.add(article)
            appitem.articles.add(article)
    #        news.articles.add(article)
            return HttpResponseRedirect(reverse("yimi_admin:news_list"))
    context = {
     #   'news': news,
        'appitem': appitem,
        'article': article,
        'out_categories': out_categories,
        'in_categories': in_categories,
    }
    return render_to_response('yimi_admin/news_add.html', context,
        context_instance=RequestContext(request))



@login_required(login_url=LOGIN_URL)
def article_detail(request, slug):
    appitem = get_appitem(request.user)
    article = appitem.articles.filter(id=slug).first()
    if not article:
        raise Http404
    context = {
        'article': article,
    }
    return render_to_response('yimi_admin/article_detail.html', context,
        context_instance=RequestContext(request))


@login_required(login_url=LOGIN_URL)
def article_delete(request, slug):
    appitem = get_appitem(request.user)
    article = appitem.articles.filter(id=slug).first()
    article.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url=LOGIN_URL)
def articles_list(request):
    appitem = get_appitem(request.user)
    slug = request.GET.get("slug")
    category = None
    if slug:
        category = appitem.categories.filter(id=slug).first()
        articles = category.articles.all()
    else:
        articles = appitem.articles.all()
    matchs, show_pages = page_turning(articles, request, 10)
    context = {
        'articles': articles,
        'category': category,
        'matchs': matchs,
        'show_pages': show_pages,
    }
    return render_to_response('yimi_admin/articles_list.html', context,
        context_instance=RequestContext(request))

#@login_required(login_url=LOGIN_URL)
#def article_update(request):
#    appitem = get_appitem(request.user)
#    article = appitem.articles.filter(id=slug).first()
#    if request.method == 'POST':
#        articleform = ArticleForm(request.POST, request.FILES, instance=article)
#        article = articleform.save()
#        category_name = request.POST.get('category')
#        category = appitem.categories.filter(name=category_name).first()
#        if not category:
#            category = appitem.categories.create(name=category_name)
#        if article not in category.articles.all():
#            category.articles.add(article)
#    context = {
#        'article': article,
#        'appitem': appitem,
#    }
#    return render_to_response('yimi_admin/article_update.html', context,
#        context_instance=RequestContext(request))

def parse_choid(choid):
    choid_list = choid.split("-")
    choid_dict = {}
    for ch in choid_list:
        choid_dict.update({ch.split('.')[0]:ch.split('.')[1]})
    return choid_dict
def parse_listchoid(listchoid):
    r1 = r'\[(\d+)\]'
    return re.findall(r1, listchoid)



@login_required(login_url=LOGIN_URL)
def reply(request):
    '''关注回复，无匹配回复，关键字编辑'''
    appitem = get_appitem(request.user)
    tag = request.GET.get('tag')
    keyword = request.GET.get('keyword') #没有值时是：关注回复，无匹配回复
    mid = request.GET.get('mid') #没有值时是：关注回复，无匹配回复
    add = request.GET.get('add') #新增关键字符号
    news_show = None
    if tag in ['keyword_default_recontent', 'subscribe']:
        message = appitem.messages.filter(tag=tag).first()
    elif mid:
        message = appitem.messages.filter(tag=tag, id=mid).first()
    elif not mid and tag == 'keyword_recontent' and add =='add':
        message = appitem.messages.create(tag='keyword_recontent')

    if message.tag == 'keyword_recontent' and not message.keyword and keyword:
        message.keyword = keyword
        message.save()
    choid = request.GET.get('choid') # '2.3-1.5-articleid.order'
    listchoid = request.GET.get('listchoid') # '[articleid.order][12]' 点击选中素材后提交

    news_articles = None
    order_dic = None
    if listchoid:
        news_articles = appitem.articles.filter(id__in=parse_listchoid(listchoid))
        news_show = request.GET.get('news_show', 'show')
    elif message.retype == 'news':
        news = message.news_set.first()
        if news.order_dic:
            order_dic = json.loads(news.order_dic)   
        news_articles = news.articles.all()
    
    field_list = ['keyword', 'tag', 'listchoid', 'news_show', 'closeshow', 'mid', 'add']
    close_show_field = ['closeshow','listchoid']
    get_data_url = convert_get_data(request.GET, field_list)
    articles = appitem.articles.all()

    page = int(request.GET.get("p",1))
    return_articles = get_entry_page(articles,10,page)
    show_pages = range(max(page-4,1),min(page+4,return_articles.paginator.num_pages)+1)

    context = {
        'message': message,
        'tag': tag,
        'news_show': news_show,
        'get_data': request.GET,
        'news_articles': news_articles,
        'order_dic': order_dic,
        'articles': articles,
        'get_data_url': get_data_url,
        'close_show_field': close_show_field,
        'show_pages': show_pages,
        'return_articles': return_articles,
        'articles': articles,
    }
    return render_to_response('yimi_admin/default_recontent.html', context,
        context_instance=RequestContext(request))


def parse_post_order_data(dic):
    end_data = {}
    for d in dic:
        if 'order' in d:
            id = d.split('-')[1]
            order = dic.get(d)
            end_data.setdefault(id, order)
    return end_data

def message_update(request):
    '''回复的所有修改和新增'''
    appitem = get_appitem(request.user)
    message_id = request.GET.get("mid")
    retype = request.GET.get("retype")
    keyword = request.GET.get("keyword")
    if message_id:
        message = appitem.messages.get(id=message_id)
    else:
        message = appitem.messages.create()
    if keyword:
        message.keyword = keyword
    if retype:
        message.retype = retype
        if retype == 'text':
            content = request.GET.get("content")
            text = message.text_set.first()
            if not text:
                text = message.text_set.create()
            text.content = content
            text.save()
            message.save()
            
        
        if request.method == 'POST':
            end_data = parse_post_order_data(request.POST)
            json_data = json.dumps(end_data)
            articles = appitem.articles.filter(id__in=end_data.keys())
            keyword = request.POST.get('keyword')
            news = message.news_set.first()
            if not news:
                news = message.news_set.create()
            for article in articles:
                if not news.articles.filter(id=article.id).exists():
                    news.articles.add(article)
            news.order_dic = json_data
            news.save()
            message.keyword = keyword
            message.save()
    return HttpResponseRedirect(reverse("yimi_admin:keyword_reply"))

@login_required(login_url=LOGIN_URL)
def keyword_reply(request):
    appitem = get_appitem(request.user)
    messages = appitem.messages.filter(tag='keyword_recontent')
    appitem.messages.filter(keyword=None, tag='keyword_recontent').delete()
 
    context = {
        'messages': messages,
    }
    return render_to_response('yimi_admin/keyword_recontent.html', context,
        context_instance=RequestContext(request))

@login_required(login_url=LOGIN_URL)
def users_list(request):
    group_id = request.GET.get('group_id')
    appitem = get_appitem(request.user)
    app_users = None
    if group_id:
        group = appitem.app_groups.get(id=group_id)
        app_users = group.app_users.all()
    else:
        app_users = appitem.app_users.all()
    app_groups = appitem.app_groups.all()
    matchs, show_pages = page_turning(app_users, request, 10)

    context = {
        'appitem': appitem,
        'app_groups': app_groups,
        'app_users': app_users,
        'matchs': matchs,
        'show_pages': show_pages,
    }
    return render_to_response('yimi_admin/users_list.html', context,
        context_instance=RequestContext(request))


@login_required(login_url=LOGIN_URL)
def groups_list(request):
    appitem = get_appitem(request.user)
    groups = appitem.app_groups.all()
    context = {
        'groups': groups,
    }
    return render_to_response('yimi_admin/groups_list.html', context,
        context_instance=RequestContext(request))

@login_required(login_url=LOGIN_URL)
def groups_delete(request):
    appitem = get_appitem(request.user)
    gid = request.GET.get('gid')
    group = appitem.app_groups.get(id=gid)
    group.delete()    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url=LOGIN_URL)
def group_name_update(request):
    appitem = get_appitem(request.user)
    gid = request.POST.get('gid')
    name = request.POST.get('name')
    status = request.POST.get('status')
    if gid and name:
        group = appitem.app_groups.get(id=gid)
        group.name = name
        if status == '1':
            group.status = True
        elif status == '0':
            group.status = False
        group.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url=LOGIN_URL)
def category_name_update(request):
    appitem = get_appitem(request.user)
    gid = request.POST.get('gid')
    name = request.POST.get('name')
    status = request.POST.get('status')

    if gid and name:
        category = appitem.categories.get(id=gid)
        category.name = name
        if status == '1':
            category.status = True
        elif status == '0':
            category.status = False
        category.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url=LOGIN_URL)
def category_remove(request):
    appitem = get_appitem(request.user)
    cate_id = request.GET.get("cate")
    art_id = request.GET.get("article")
    category = appitem.categories.filter(id=cate_id).first()
    article = appitem.articles.filter(id=art_id).first()
    category.articles.remove(article)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url=LOGIN_URL)
def category_delete(request):
    appitem = get_appitem(request.user)
    gid = request.GET.get('gid')
    category = appitem.categories.get(id=gid)
    category.delete()    
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url=LOGIN_URL)
def category_add(request):
    category_name = request.GET.get('name')
    status = request.GET.get('status')
    if category_name:
        appitem = get_appitem(request.user)
        category = appitem.categories.filter(name=category_name).first()

        if status == '1':
            category_status = True
        elif status == '0':
            category_status = False
        if not category:
            appitem.categories.create(name = category_name, status=category_status)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url=LOGIN_URL)
def groups_add(request):
    group_name = request.GET.get('name')
    status = request.GET.get('status')
    if group_name:
        appitem = get_appitem(request.user)
        if status == '1':
            group_status = True
        elif status == '0':
            group_status = False
        group = appitem.app_groups.filter(name=group_name).first()
        if not group:
            appitem.app_groups.create(name=group_name, status=group_status)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
@login_required(login_url=LOGIN_URL)
def group_update(request):
    '''用户新加入组'''
    group_id = request.GET.get('groupid')
    user_id = request.GET.get('userid')
    if group_id and user_id:
        appitem = get_appitem(request.user)
        group = appitem.app_groups.filter(id=group_id).first()
        user = appitem.app_users.filter(id=user_id).first()
        if user not in group.app_users.all():
            group.app_users.add(user)
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url=LOGIN_URL)
def group_remove(request):
    group_id = request.GET.get('groupid')
    user_id = request.GET.get('userid')
    if group_id and user_id:
        appitem = get_appitem(request.user)
        group = appitem.app_groups.filter(id=group_id).first()
        user = appitem.app_users.filter(id=user_id).first()
        if user in group.app_users.all():
            group.app_users.remove(user)
        
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url=LOGIN_URL)
def menus_list(request):
    appitem = get_appitem(request.user)
    context = {
        'appitem': appitem,
    }
    SubButton.objects.filter(menubutton__appitem=appitem, name=None).delete()
    appitem.menu_buttons.filter(name=None).delete()
    return render_to_response('yimi_admin/menus_list.html', context,
        context_instance=RequestContext(request))

@login_required(login_url=LOGIN_URL)
def menu_update(request):
    '''一级菜单修改'''
    menu_id = request.GET.get('menuid')
    appitem = get_appitem(request.user)
    messages = appitem.messages.filter(tag='keyword_recontent')
    if menu_id:
        menu = appitem.menu_buttons.get(id=menu_id)
        message = None
        sub_buttons = None
        if menu.type == 'click' and menu.key:
            message = appitem.messages.filter(keyword=menu.key, tag='keyword_recontent').first() 
        elif menu.type == 'sub_button':
            sub_buttons = menu.sub_button.all()
            
        context = {
            'menu': menu,
            'messages': messages,
            'message': message,
            'sub_menus': sub_buttons,
            'menu_id': menu_id,
        }
    else:
        context = {'messages': messages,}
    return render_to_response('yimi_admin/menu_editor.html', context,
        context_instance=RequestContext(request))

@login_required(login_url=LOGIN_URL)
def menu_click(request):
    '''按键及子按键的click事件修改'''
    menu_id = request.GET.get('menuid')
    type = request.GET.get('type')  #区分是菜单还是子菜单
    message_id = request.GET.get('messageid')
    menu_name = request.GET.get('name')
    if menu_id and type and message_id:
        appitem = get_appitem(request.user)
        message = appitem.messages.get(id=message_id)
        if type == 'menu':
            menu = appitem.menu_buttons.get(id=menu_id)
            menu.key = message.keyword
            menu.type = 'click'
            menu.name = menu_name
            menu.save()
        elif type == 'submenu':
            #先判断是否是当前appitem的子按键
            sub_menu = SubButton.objects.get(id=menu_id)
            if sub_menu.menubutton_set.first().appitem_set.first() == appitem:
                sub_menu.type = 'click'
                sub_menu.key = message.keyword
                sub_menu.name = menu_name
                sub_menu.save()   
    redirct = reverse("yimi_admin:menus_list")
    return HttpResponseRedirect(redirct)


@login_required(login_url=LOGIN_URL)
def menu_url(request):
    '''按键及子按键的view事件修改'''
    menu_id = request.POST.get('menuid')
    url = request.POST.get('url')
    type = request.POST.get('type')
    menu_name = request.POST.get('name')
    appitem = get_appitem(request.user)
    if menu_id and url and not type:
        menu = appitem.menu_buttons.get(id=menu_id)
        menu.type = 'view'
        menu.url = url
        menu.name = menu_name
        menu.save()
    elif type:
        sub_menu = SubButton.objects.get(id=menu_id)
        if sub_menu.menubutton_set.first().appitem_set.first() == appitem:
            sub_menu.type = 'view'
            sub_menu.url = url
            sub_menu.name = menu_name
            sub_menu.save()

    redirct = reverse("yimi_admin:menus_list")
    return HttpResponseRedirect(redirct)


@login_required(login_url=LOGIN_URL)
def menu_change_name(request):
    '''按键及子按键改名'''
    menu_id = request.GET.get("menuid")
    tag = request.GET.get("tag")
    name = request.GET.get("name")

    if menu_id and tag:
        appitem = get_appitem(request.user)
        if tag == 'menu':
            menu = appitem.menu_buttons.get(id=menu_id)
            menu.name = name
            menu.save()
        elif tag == "submenu":
            sub_menu = SubButton.objects.get(id=menu_id)
            if sub_menu.menubutton_set.first().appitem_set.first() == appitem:
                sub_menu.name = name
                sub_menu.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    

@login_required(login_url=LOGIN_URL)
def menu_add(request):
    '''增加按键'''
    appitem = get_appitem(request.user)
    messages = appitem.messages.filter(tag='keyword_recontent')
    menu = appitem.menu_buttons.create()
    context = {
        'messages': messages,
        'menu': menu,
    }
    return render_to_response('yimi_admin/menu_editor.html', context,
        context_instance=RequestContext(request))

@login_required(login_url=LOGIN_URL)
def menu_delete(request):
    '''删除按键及子按键'''
    appitem = get_appitem(request.user)
    menu_id = request.GET.get('menuid')
    type = request.GET.get('type')
    if type == 'menu':
        menu = appitem.menu_buttons.get(id=menu_id)
        menu.sub_button.all().delete()
        menu.delete()
    elif type == 'submenu':
        sub_menu = SubButton.objects.get(id=menu_id)
        if sub_menu.menubutton_set.first().appitem_set.first() == appitem:
            sub_menu.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url=LOGIN_URL)
def sub_menu_update(request):
    sub_menu_id = request.GET.get('submenuid')
    menu_id = request.GET.get('menuid')
    name = request.GET.get('name')
    appitem = get_appitem(request.user)
    messages = appitem.messages.filter(tag='keyword_recontent')
    if sub_menu_id and menu_id:
        sub_menu = SubButton.objects.get(id=sub_menu_id)
        menu = appitem.menu_buttons.get(id=menu_id)
        if name:
            menu.name = name
            menu.save()
        if sub_menu in menu.sub_button.all():
            message = sub_menu.get_message()
            context = {
                'sub_menu': sub_menu,
                'message': sub_menu.get_message(),
                'messages': messages,
                'sub_menu_id': sub_menu_id,
            }
    
    else:
        context = {
            'messages': messages,
        }
    return render_to_response('yimi_admin/sub_menu_editor.html', context,
        context_instance=RequestContext(request))


@login_required(login_url=LOGIN_URL)
def sub_menu_add(request):
    menu_id = request.GET.get('menuid')
    name = request.GET.get('name')
    appitem = get_appitem(request.user)
    menu = appitem.menu_buttons.get(id=menu_id)
    menu.type = 'sub_button'
    menu.name = name
    menu.save()
    sub_menu = menu.sub_button.create()
    menu.sub_button.add(sub_menu)
    messages = appitem.messages.filter(tag='keyword_recontent')
    context = {
        'sub_menu': sub_menu,
        'messages': messages,
        'menu': menu
    }
    return render_to_response('yimi_admin/sub_menu_editor.html', context,
        context_instance=RequestContext(request))

@login_required(login_url=LOGIN_URL)
def text_update(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        slug = int(request.POST.get('slug'))
        message = Message.objects.get(id=slug)
        keyword = request.POST.get('keyword')
        if keyword:
            message.keyword = keyword
        text = message.text_set.first()
        if text:
            text.content = content
            text.save()
        else:
            text = message.text_set.create(content= content)
        message.retype = 'text'
        message.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url=LOGIN_URL)
def news_update(request):
    news_id = request.GET.get('n')
    message_id = request.GET.get('message')
    appitem = get_appitem(request.user)
    news = appitem.news.get(id=news_id)
    keyword = request.GET.get('keyword')
    message = appitem.messages.get(id=message_id)
    if keyword:
        message.keyword = keyword
    message.retype = 'news'
    message.save()

    news.messages.add(message)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url=LOGIN_URL)
def keyword_add(request):
    appitem = get_appitem(request.user)
    news_id = request.GET.get("n")      
    if news_id:
        new = appitem.news.get(id=news_id)
        keyword = request.GET.get('keyword')
        if keyword:
            message = appitem.messages.create(retype="news", keyword=keyword)
            new.messages.add(message)
            return HttpResponseRedirect(reverse('yimi_admin:keyword_reply'))
    if request.method == 'POST':
        content = request.POST.get('content')
        keyword = request.POST.get('keyword')
        if content and keyword:
            message = appitem.messages.create(retype="text", keyword=keyword)
            message.text_set.create(content=content)
            return HttpResponseRedirect(reverse('yimi_admin:keyword_reply'))
    news = appitem.news.exclude(articles=None)
    context = {
        'appitem': appitem,
        'news': news,
    }
    return render_to_response('yimi_admin/keyword_add.html', context,
        context_instance=RequestContext(request))

@login_required(login_url=LOGIN_URL)
def keyword_delete(request):
    appitem = get_appitem(request.user)
    mid = request.GET.get('mid')
    message = appitem.messages.get(id=mid)
    if message.retype == 'text':
        message.text_set.all().delete()
    message.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url=LOGIN_URL)
def send_create_menu(request):
    if get_appitem(request.user).send_create_menu():
        return_data = {'error': 0}
    else:
        return_data = {"error": 1}
    json_data = json.dumps(return_data)
    return HttpResponse(json_data, content_type="application/json")
    


@login_required(login_url=LOGIN_URL)
def activity_list(request):
    appitem = get_appitem(request.user)
    activities = appitem.activity_set.all()
    context = {'appitem': appitem, 'activities': activities}
    return render_to_response('yimi_admin/activity_list.html', context,
        context_instance=RequestContext(request))


@login_required(login_url=LOGIN_URL)
def open_account_list(request):
    appitem = get_appitem(request.user)
    open_accounts = appitem.openaccount_set.all()
    context = {
        'accounts': open_accounts,
        'appitem': appitem,
        'tag': 'open_account',
    }
    return render_to_response('yimi_admin/account_list.html', context,
        context_instance=RequestContext(request))

@login_required(login_url=LOGIN_URL)
def sim_account_list(request):
    appitem = get_appitem(request.user)
    sim_accounts = appitem.simaccount_set.all()
    context = {
        'appitem': appitem,
        'accounts': sim_accounts,
        'tag': 'sim_account',
    }
    return render_to_response('yimi_admin/account_list.html', context,
        context_instance=RequestContext(request))

@login_required(login_url=LOGIN_URL)
def activity_account_list(request, aid):
    appitem = get_appitem(request.user)

    activity = appitem.activity_set.get(id=aid)
    activity_users = activity.activity_users.all
    context = {
        'appitem': appitem,
        'accounts': activity_users,
        'tag': 'activity_account',
        'activity': activity
    }
    return render_to_response('yimi_admin/account_list.html', context,
        context_instance=RequestContext(request))


@login_required(login_url=LOGIN_URL)
def activity_add(request):
    appitem = get_appitem(request.user)
    aid = request.GET.get("aid")
    if aid:
        activity = appitem.activity_set.get(id=aid)
    else:
        activity = None
    if request.method == 'POST':
        title = request.POST.get('title')
        a_time = request.POST.get('a_time')
        count = request.POST.get('count')
        xingshi = request.POST.get('xingshi')
        place = request.POST.get('place')
        speaker = request.POST.get('speaker')
        content = request.POST.get('content')
        if activity:
            activity.title = title
            activity.a_time = a_time
            activity.xingshi = xingshi
            activity.place = place
            activity.speaker = speaker
            activity.count = count
            activity.content = content
            activity.save()
        else:
            appitem.activity_set.create(
                title=title, 
                a_time=a_time, 
                count=count,
                xingshi = xingshi,
                place = place,
                speaker = speaker,
                content = content,
            )
        return HttpResponseRedirect(reverse("yimi_admin:activity_list"))
    
    context = {
        'appitem': appitem,
        'activity': activity,
    }
    return render_to_response('yimi_admin/activity_add.html', context,
        context_instance=RequestContext(request))


@login_required(login_url=LOGIN_URL)
def activity_delete(request, id):
    appitem = get_appitem(request.user)
    activity = appitem.activity_set.filter(id=id)
    if activity:
        activity.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    
@login_required(login_url=LOGIN_URL)
def account_delete(request, tag, id):
    appitem = get_appitem(request.user)
    if tag == 'sim_account':
        sim_account = appitem.simaccount_set.get(id=id)
        sim_account.delete()
    elif tag == 'open_account':
        open_account = appitem.openaccount_set.get(id=id)
        open_account.delete()
    elif tag == 'activity_account':
        aa = ActivityUser.objects.get(id=id)
        activity = aa.activity_set.first()
        if activity.appitem == appitem:
            aa.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url=LOGIN_URL)
def activity_status(request, id):
    appitem = get_appitem(request.user)
    activity = appitem.activity_set.get(id=id)
    if activity.status:
        activity.status = False
    else:
        activity.status = True
    activity.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@login_required(login_url=LOGIN_URL)
def questions_list(request):
    appitem = get_appitem(request.user)
    kefus = appitem.kefu_set.all()
    direct_url = 'http://'+ appitem.domain + reverse("nanjing:show_question", args=(appitem.slug,))
    base_url = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid='+appitem.appid+'&redirect_uri=%s&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect' 
    url = base_url % direct_url
    context = {
        'appitem': appitem,
        'kefus': kefus,
        'url':url
    }
    return render_to_response('yimi_admin/questions_list.html', context,
        context_instance=RequestContext(request))

@login_required(login_url=LOGIN_URL)
def answer_question(request):
    appitem = get_appitem(request.user)
    qid = request.POST.get('qid')
    kefu = appitem.kefu_set.get(id=qid)
    answer = request.POST.get('answer')
    kefu.answer = answer
    kefu.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@login_required(login_url=LOGIN_URL)
def kefu_delete(request):
    appitem = get_appitem(request.user)
    gid = request.GET.get("gid", '')
    kefu = appitem.kefu_set.get(id=gid)
    kefu.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
