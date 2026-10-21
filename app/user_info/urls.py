# /app/user_info/url.py

"""
URL mapping for the USer Info App
"""
from django.urls import path
from user_info import views

app_name = "user_info"
urlpatterns = [
    #
    path('user_profile_step1',   views.user_profile_step1, name='user_profile_step1'),
    path('user_profile_step2',   views.user_profile_step2, name='user_profile_step2'),
    path('user_profile_mfa',     views.user_profile_mfa,   name='user_profile_mfa'),
    path('user_login',           views.user_login,         name='user_login'),
    path('user_pwd_rst_step1',   views.user_pwd_rst_step1, name='user_pwd_rst_step1'),
    path('user_pwd_rst_step2',   views.user_pwd_rst_step2, name='user_pwd_rst_step2'),
    path('user_pwd_rst_mfa',     views.user_pwd_rst_mfa,   name='user_pwd_rst_mfa'),
    path('user_logout',          views.user_logout,        name='user_logout'),
    path('user_admin',           views.user_admin,         name='user_admin'),
    path('user_delete/<int:id>', views.user_delete,        name='user_delete'),

    path('myplant_db_xfer',      views.myplant_db_xfer,    name='myplant_db_xfer'),
]