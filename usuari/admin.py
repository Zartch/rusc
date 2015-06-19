__author__ = 'Zartch'
from django.contrib import admin
from usuari.models import UserProfile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

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
    list_display = ('user','website','avatar','cela','estat','email_p')
    search_fields = ['user']
    list_filter = ['user']

admin.site.register(UserProfile, UsuariAdmin)