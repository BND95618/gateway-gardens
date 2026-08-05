# app/pests/urls.py
"""
URL mapping for the Pests App
"""
from django.urls import path
from pests       import views

app_name = "pests"
urlpatterns = [
    path('pest_summary',          views.pest_summary, name="pest_summary"),
    path('pest_details/<int:id>', views.pest_details, name="pest_details"),
    path('pest_add',              views.pest_add,     name="pest_add"),
    path('pest_edit/<int:id>',    views.pest_edit,    name="pest_edit"),
    path('pest_delete/<int:id>',  views.pest_delete,  name="pest_delete"),
]