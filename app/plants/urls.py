"""
URL mapping for the Plants App
"""
from django.urls import path
from plants import views

app_name = "plants"
urlpatterns = [
    path('',                        views.index,            name='index'),
    path('gardens_summary',         views.gardens_summary,  name='gardens_summary'),
    path('gardens_add',             views.gardens_add,      name="gardens_add"),
    path('gardens_update/<int:id>', views.gardens_update,   name="gardens_update"),
    path('myplants_summary',        views.myplants_summary, name='myplants_summary'),
    path('plants_search',           views.plants_search,    name='plants_search'),
    path('plants_glossary',         views.plants_glossary,  name='plants_glossary'),
    path('plants_reference',        views.plants_reference, name='plants_reference'),
    path('plants_about',            views.plants_about,     name='plants_about'),
    path('user_signup',             views.user_signup,      name='user_signup'),
    path('user_login',              views.user_login,       name='user_login'),
    path('user_logout',             views.user_logout,      name='user_logout'),
]