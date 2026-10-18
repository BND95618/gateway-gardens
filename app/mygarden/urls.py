"""
URL mapping for the Mygarden App
"""
from django.urls import path
from mygarden import views

app_name = "mygarden"
urlpatterns = [
    path('mygarden_summary',         views.mygarden_summary,         name='mygarden_summary'),
    path('mygarden_add',             views.mygarden_add,             name="mygarden_add"),
    path('mygarden_edit/<int:id>',   views.mygarden_edit,            name="mygarden_edit"),
    #
    path('mygarden_plan',            views.mygarden_plan,            name='mygarden_plan'),
    path('mygarden_plan_edit_modal', views.mygarden_plan_edit_modal, name='mygarden_plan_edit_modal'),
    path('plant_details_modal',      views.plant_details_modal,      name='plant_details_modal'),
    path('plant_fetch',              views.plant_fetch,              name='plant_fetch'),
    #
    path('mygarden_todo',                  views.mygarden_todo,             name='mygarden_todo'),
    path('mygarden_todo_details/<int:id>', views.mygarden_todo_details,     name='mygarden_todo_details'),
    path('mygarden_todo_add/<int:id>',     views.mygarden_todo_add,         name='mygarden_todo_add'),
    path('mygarden_todo_edit/<int:id>',    views.mygarden_todo_edit,        name='mygarden_todo_edit'),
    path('mygarden_todo_del/<int:id>',     views.mygarden_todo_del,         name='mygarden_todo_del'),
    path('mygarden_todo_done/<int:id>',    views.mygarden_todo_done,        name='mygarden_todo_done'),
    path('mygarden_todo_save/<int:id>',    views.mygarden_todo_save,        name='mygarden_todo_save'),
    path('mygarden_todo_fetch',            views.mygarden_todo_fetch,       name='mygarden_todo_fetch'),
]