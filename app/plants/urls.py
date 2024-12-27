"""
URL mapping for the Plants App
"""
from django.urls import path
from plants import views

app_name = "plants"
urlpatterns = [
    path('',                          views.index,            name='index'),
    path('gardens_summary',           views.gardens_summary,  name='gardens_summary'),
    path('gardens_add',               views.gardens_add,      name="gardens_add"),
    path('gardens_update/<int:id>',   views.gardens_update,   name="gardens_update"),
    path('myplants_add/<int:id>',     views.myplants_add,     name='myplants_add'),
    path('myplants_update/<int:id>',  views.myplants_update,  name='myplants_update'),
    path('myplants_delete/<int:id>',  views.myplants_delete,  name='myplants_delete'),
    path('myplants_remove/<int:id>',  views.myplants_remove,  name='myplants_remove'),
    path('myplants_summary',          views.myplants_summary, name='myplants_summary'),
    path('myplants_details/<int:id>', views.myplants_details, name='myplants_details'),
    path('myplants_comment/<int:id>', views.myplants_comment, name='myplants_comment'),
    path('plant2garden/<int:id>',     views.plant2garden,     name='plant2garden'),
    path('plants_search',             views.plants_search,    name='plants_search'),
    path('plants_add',                views.plants_add,       name='plants_add'),
    path('plants_details/<int:id>',   views.plants_details,   name='plants_details'),
    path('plants_comment/<int:id>',   views.plants_comment,   name='plants_comment'),
    path('plants_update/<int:id>',    views.plants_update,    name='plants_update'),
    path('plants_delete/<int:id>',    views.plants_delete,    name='plants_delete'),
    path('plants_glossary',           views.plants_glossary,  name='plants_glossary'),
    path('plants_reference',          views.plants_reference, name='plants_reference'),
    path('plants_about',              views.plants_about,     name='plants_about'),
    path('user_signup',               views.user_signup,      name='user_signup'),
    path('user_login',                views.user_login,       name='user_login'),
    path('user_update',               views.user_update,      name='user_update'),
    path('user_recovery',             views.user_recovery,    name='user_recovery'),
    path('user_logout',               views.user_logout,      name='user_logout'),
    # views for debug and testing purposes
    path('debug',                     views.debug,            name='debug'),
    path('fiddle',                    views.fiddle,           name='fiddle'),
]