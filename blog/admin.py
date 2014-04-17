from django.contrib import admin
from models import *

class DataAdmin(admin.ModelAdmin):
    list_display = ['keyword', 'content']
    search_fields = ['keyword']

class AppItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_weixin_api']
class AppUserAdmin(admin.ModelAdmin):
    search_fields = ['nickname']
    list_display = ['nickname', 'openid']

admin.site.register(Message)
admin.site.register(Text)
admin.site.register(News)
admin.site.register(Article)
admin.site.register(AppUser, AppUserAdmin)
admin.site.register(AppGroup)
admin.site.register(AppItem, AppItemAdmin)
admin.site.register(MenuButton)
admin.site.register(SubButton)
admin.site.register(QRCode)
admin.site.register(Category)
admin.site.register(KeFu)
