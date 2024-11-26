from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect # Added for images
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Garden, Plant, Comment
from .forms  import GardenAddUpdateForm, PlantAddUpdateForm, PlantCommentForm

import math
import os

# Define attribute select options
plant_types      = ["tbd", "Annual", "Grass", "Groundcover", "Perennial", "Shrub", "Succulent", "Tree", "Vegetable", "Vine"]
sun_exposure_opt = ["tbd", "Full Sun", "Partial Sun", "Partial Shade", "Full Shade"]
water_rqmts_opt  = ["tbd", "Very Low", "Low", "Medium", "High", "Very High"]
bloom_color_opt  = ["tbd", "white", "red", "pink", "green", "blue", "orange"]
bloom_season_opt = ["tbd", "Spring", "Summer", "Fall", "Winter", "None"]
pollinators_opt  = ["tbd", "Bees", "Butterfiles", "Hummingbirds", "None"]
ca_native_opt    = ["tbd", "Yes", "No"]
usda_zones       = ["tbd", "1a", "1b", "2a", "2b", "3a", "3b", "4a", "4b", "5a", "5b", "6a", "6b", "7a", "7b", 
                    "8a", "8b", "9a", "9b", "10a", "10b"]
# sunset_zones     = list(range(1, 25))

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