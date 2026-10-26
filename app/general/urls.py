# /app/general/urls.py
"""
URL mapping for the General App
"""
from django.urls import path
from general     import views

app_name = "general"
urlpatterns = [
    path('',           views.index,     name='index'),
    
    path('glossary/',  views.glossary,  name='glossary'),
    path('reference/', views.reference, name='reference'),
    path('about/',     views.about,     name='about'),
    # views for debug and testing purposes
    path('debug/',     views.debug,     name='debug'),
    path('fiddle/',    views.fiddle,    name='fiddle'),
]