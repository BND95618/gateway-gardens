# /app/user_info/admin.py

from django.contrib import admin

from django.contrib   import admin
from user_info.models import UserInfo
    
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ("user",)

admin.site.register(UserInfo, UserInfoAdmin)