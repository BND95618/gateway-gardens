from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect # Added for images
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#
from django.contrib.auth.models import User                        # User signup
from django.contrib.auth        import authenticate, login, logout # User login/logout

from .models import Garden, Plant, Comment
from .forms  import UserSignupForm, UserLoginForm
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

# Home page view
@login_required
def gardens_summary(request):
    """ Render the Garden Summary page for Gateway Gardens app """
    gardens = Garden.objects.all()
    template = loader.get_template("plants/gardens_summary.html")
    context = {}
    # AR: If  user has > 1 garden then add garden selection code 
    my_gardens = 0
    all_gardens = 0
    for garden in gardens:
        if garden:
             all_gardens = all_gardens + 1
             if (request.user.username == garden.owner):
                context = { "garden" : garden }
                my_gardens = my_gardens + 1
        else:                                                   # no user has a garden in db
            return HttpResponseRedirect(reverse('plants:gardens_add')) 
    if my_gardens == 0:                                         # current user has no gardens in db
        return HttpResponseRedirect(reverse('plants:gardens_add')) 
    return HttpResponse(template.render(context, request))


    #return render(request, 'plants/gardens_summary.html')

# Add garden to the database
@login_required
def gardens_add(request):
    """ AR """
    garden = Garden()
    if request.POST:
        form = GardenAddUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            garden.name        = form.cleaned_data.get('name')
            garden.city        = form.cleaned_data.get('city')
            garden.state       = form.cleaned_data.get('state')
            garden.owner       = request.user.username
            garden.usda_zone   = form.cleaned_data.get('usda_zone')
            garden.sunset_zone = form.cleaned_data.get('sunset_zone')

            if 'image_1' in request.FILES:
                garden.image_1   = request.FILES['image_1']
                garden.caption_1 = form.cleaned_data.get('caption_1')
            if 'image_2' in request.FILES:
                garden.image_2   = request.FILES['image_2']
                garden.caption_2 = form.cleaned_data.get('caption_2')
            if 'image_3' in request.FILES:
                garden.image_3   = request.FILES['image_3']
                garden.caption_3 = form.cleaned_data.get('caption_3')
            if 'image_4' in request.FILES:
                garden.image_4   = request.FILES['image_4']
                garden.caption_4 = form.cleaned_data.get('caption_4')
            if 'image_5' in request.FILES:
                garden.image_5   = request.FILES['image_5']
                garden.caption_5 = form.cleaned_data.get('caption_5')
            if 'image_6' in request.FILES:
                garden.image_6   = request.FILES['image_6']
                garden.caption_6 = form.cleaned_data.get('caption_6')
            if 'image_7' in request.FILES:
                garden.image_7   = request.FILES['image_7']
                garden.caption_7 = form.cleaned_data.get('caption_7')
            if 'image_8' in request.FILES:
                garden.image_8   = request.FILES['image_8']
                garden.caption_8 = form.cleaned_data.get('caption_8')

            garden.save()
        return HttpResponseRedirect(reverse('plants:gardens_summary'))
    else:
        form = GardenAddUpdateForm()
        context = { 'form' : form }
        return render(request, 'plants/gardens_add.html', context)

# Update garden details
@login_required
def gardens_update(request, id):
    """ AR """
    garden = Garden.objects.get(id=id)
    if request.POST:
        form = GardenAddUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            garden.name        = form.cleaned_data.get('name')
            garden.city        = form.cleaned_data.get('city')
            garden.state       = form.cleaned_data.get('state')
            garden.owner       = request.user.username
            garden.usda_zone   = form.cleaned_data.get('usda_zone')
            garden.sunset_zone = form.cleaned_data.get('sunset_zone')

            if 'image_1' in request.FILES:
                if (garden.image_1):
                    os.remove(garden.image_1.path)
                garden.image_1   = request.FILES['image_1']
                garden.caption_1 = form.cleaned_data.get('caption_1')
            if 'image_2' in request.FILES:
                if (garden.image_2):
                    os.remove(garden.image_2.path)
                garden.image_2   = request.FILES['image_2']
                garden.caption_2 = form.cleaned_data.get('caption_2')
            if 'image_3' in request.FILES:
                if (garden.image_3):
                    os.remove(garden.image_3.path)
                garden.image_3   = request.FILES['image_3']
                garden.caption_3 = form.cleaned_data.get('caption_3')
            if 'image_4' in request.FILES:
                if (garden.image_4):
                    os.remove(garden.image_4.path)
                garden.image_4   = request.FILES['image_4']
                garden.caption_4 = form.cleaned_data.get('caption_4')
            if 'image_5' in request.FILES:
                if (garden.image_5):
                    os.remove(garden.image_5.path)
                garden.image_5   = request.FILES['image_5']
                garden.caption_5 = form.cleaned_data.get('caption_5')
            if 'image_6' in request.FILES:
                if (garden.image_6):
                    os.remove(garden.image_6.path)
                garden.image_6   = request.FILES['image_6']
                garden.caption_6 = form.cleaned_data.get('caption_6')
            if 'image_7' in request.FILES:
                if (garden.image_7):
                    os.remove(garden.image_7.path)
                garden.image_7   = request.FILES['image_7']
                garden.caption_7 = form.cleaned_data.get('caption_7')
            if 'image_8' in request.FILES:
                if (garden.image_8):
                    os.remove(garden.image_8.path)
                garden.image_8   = request.FILES['image_8']
                garden.caption_8 = form.cleaned_data.get('caption_8')

            garden.save()
        return HttpResponseRedirect(reverse('plants:gardens_summary'))
    else:
        # set the update form with the current db values
        form = GardenAddUpdateForm(initial={ 'name'        : garden.name,
                                             'city'        : garden.city,
                                             'state'       : garden.state,
                                             'usda_zone'   : garden.usda_zone,
                                             'sunset_zone' : garden.sunset_zone,
                                             'image_1'     : garden.image_1,
                                             'caption_1'   : garden.caption_1,
                                             'image_2'     : garden.image_2,
                                             'caption_2'   : garden.caption_2,
                                             'image_3'     : garden.image_3,
                                             'caption_3'   : garden.caption_3,
                                             'image_4'     : garden.image_4,
                                             'caption_4'   : garden.caption_4,
                                             'image_5'     : garden.image_5,
                                             'caption_5'   : garden.caption_5,
                                             'image_6'     : garden.image_6,
                                             'caption_6'   : garden.caption_6,
                                             'image_7'     : garden.image_7,
                                             'caption_7'   : garden.caption_7,
                                             'image_8'     : garden.image_8,
                                             'caption_8'   : garden.caption_8,
                                           })
        context = { 'garden' : garden, 
                    'form' : form,
                  }
        return render(request, 'plants/gardens_update.html', context)

# My Plants page  
@login_required
def myplants_summary(request):
    """ Render the My Plants page for Gateway Gardens app """
    # AR: Under construction
    plants = Plant.objects.all().values() 
    # if Plant.objects.filter(gardens__garden_owner=request.user.username):
    #     plants = Plant.objects.filter(gardens__garden_owner=request.user.username)
    template = loader.get_template("plants/myplants_summary.html")
    context = { "plants" : plants }
    return HttpResponse(template.render(context, request))

@login_required
def plants_search(request):
    """ Render the Plants Search for Gateway Gardens app """
    return render(request, 'plants/plants_search.html')

@login_required
def plants_glossary(request):
    """ Render the Glossary Page for Gateway Gardens app """
    return render(request, 'plants/plants_glossary.html')

@login_required
def plants_reference(request):
    """ Render the Reference Page for Gateway Gardens app """
    return render(request, 'plants/plants_reference.html')

@login_required
def plants_about(request):
    """ Render the About Page for Gateway Gardens app """
    return render(request, 'plants/plants_about.html')

def user_signup(request):
    """ Render the User Signup Page for Gateway Gardens app """
    if request.POST:
        form = UserSignupForm(request.POST)
        if form.is_valid():
            username   = form.cleaned_data.get('username')
            password   = form.cleaned_data.get('password')
            email      = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name  = form.cleaned_data.get('last_name')
            # AR: Check validity of username (unique, characters) and handle appropriately
            # AR: Handle case where password is unuseable
            # AR: Handle case where email is unuseable 
            user = User.objects.create_user(username, email, password)
            user.first_name = first_name
            user.last_name  = last_name
            user.save()
        return render(request, 'plants/user_login.html')
    else:
        form = UserSignupForm()
        context = { 'form' : form }
        return render(request, 'plants/user_signup.html', context)
    
def user_login(request):
    """ Render the User Login Page for Gateway Gardens app """
    if request.POST:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username   = form.cleaned_data.get('username')
            password   = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'plants/index.html')
            else:
                # AR: create message and return to login page
                return render(request, 'plants/user_login.html')
    else:
        form = UserLoginForm()
        context = { 'form' : form }
        return render(request, 'plants/user_login.html', context)
    
def user_logout(request):
    """ User Logout function for Gateway Gardens app """
    logout(request)
    return render(request, 'plants/index.html')
