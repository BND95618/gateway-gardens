"""
URL mapping for the Plants App
"""
from django.urls import path
from plants      import views

app_name = "plants"
urlpatterns = [
    path('',                               views.index,                    name='index'),
    #
    path('plants_summary',                 views.plants_summary,            name='plants_summary'),
    path('plant2garden/<int:id>',          views.plant2garden,              name='plant2garden'),
    path('plants_glossary',                views.plants_glossary,           name='plants_glossary'),
    path('plants_reference',               views.plants_reference,          name='plants_reference'),
    path('plants_about',                   views.plants_about,              name='plants_about'),
    #
    path('plant_add',                      views.plant_add,                 name='plant_add'),
    path('plant_edit/<int:id>',            views.plant_edit,                name='plant_edit'),
    path('plant_details/<int:id>',         views.plant_details,             name='plant_details'),
    path('plant_comment/<int:id>',         views.plant_comment,             name='plant_comment'),
    path('plant_delete/<int:id>',          views.plant_delete,              name='plant_delete'),
    #
    path('column_chooser',                 views.column_chooser,            name='column_chooser'),
    #
    path('plants_glossary',                views.plants_glossary,           name='plants_glossary'),
    path('plants_reference',               views.plants_reference,          name='plants_reference'),
    path('plants_about',                   views.plants_about,              name='plants_about'),
    # views for debug and testing purposes
    path('debug',                          views.debug,                     name='debug'),
    path('fiddle',                         views.fiddle,                    name='fiddle'),
]