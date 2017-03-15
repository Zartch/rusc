# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from xarxa.usuari.models import UserProfile, UserInfo


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'userprofile'

# Define a new User admin
class UserProfileAdmin(UserAdmin):
    inlines = (UserProfileInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class UsuariAdmin(admin.ModelAdmin):
    list_display = ('user','website','avatar','cela','estat','email_p','get_etq')
    search_fields = ['user']
    list_filter = ['user']
    filter_horizontal = ('subscripcions',)

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('usr','etq','visible')
    search_fields = ['usr','etq']
    list_filter = ['usr','etq','visible']

admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(UserProfile, UsuariAdmin)