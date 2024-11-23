from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect # Added for images
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# from .models import Garden, Plant, Comment
# from .forms  import GardenAddUpdateForm, PlantAddUpdateForm, PlantCommentForm

import math
import os

def index(request):
    """ Render the landing page for Gateway Gardens app """
    return render(request, 'plants/index.html')

# @login_required(login_url='/accounts/login/')
def gardens_summary(request):
    """ Render the Garden Summary page for Gateway Gardens app """
    return render(request, 'plants/gardens_summary.html')

# @login_required(login_url='/accounts/login/')
def myplants_summary(request):
    """ Render the My Plants page for Gateway Gardens app """
    return render(request, 'plants/myplants_summary.html')

# @login_required(login_url='/accounts/login/')
def plants_search(request):
    """ Render the Plants Search for Gateway Gardens app """
    return render(request, 'plants/plants_search.html')

# @login_required(login_url='/accounts/login/')
def plants_glossary(request):
    """ Render the Glossary Page for Gateway Gardens app """
    return render(request, 'plants/plants_glossary.html')

# @login_required(login_url='/accounts/login/')
def plants_reference(request):
    """ Render the Reference Page for Gateway Gardens app """
    return render(request, 'plants/plants_reference.html')

# @login_required(login_url='/accounts/login/')
def plants_about(request):
    """ Render the About Page for Gateway Gardens app """
    return render(request, 'plants/plants_about.html')