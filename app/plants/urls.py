"""
URL mapping for the Plants App
"""
from django.urls import path
from plants import views

app_name = "plants"
urlpatterns = [
    path('',                        views.index,            name='index'),
    path('gardens_summary',         views.gardens_summary,  name='gardens_summary'),
    path('myplants_summary',        views.myplants_summary, name='myplants_summary'),
    path('plants_search',           views.plants_search,    name='plants_search'),
    path('plants_glossary',         views.plants_glossary,  name='plants_glossary'),
    path('plants_reference',        views.plants_reference, name='plants_reference'),
    path('plants_about',            views.plants_about,     name='plants_about'),
]