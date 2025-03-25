from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect # Added for images
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#
from django.contrib.auth.models import User, Group                 # User signup
from django.contrib.auth        import authenticate, login, logout # User login/logout

from email_validator import validate_email

from .models import Garden, MyPlant, Plant, Comment, MyPlantComment, Pest
from .forms  import UserSignupForm, UserLoginForm, UserUpdateForm, UserRecoveryForm, ColumnChooserForm, MyColumnChooserForm
from .forms  import GardenAddUpdateForm, MyPlantAddUpdateForm, MyPlantCommentForm
from .forms  import PlantAddUpdateForm, PlantCommentForm
from .forms  import PestAddUpdateForm

import math
import os

# Define attribute select option arrays
plant_types      = ["tbd", "Annual", "Fern", "Grass", "Groundcover", "Perennial", "Shrub", 
                    "Succulent", "Tree", "Vegetable", "Vine"]
bloom_color_opt  = ["tbd", "white", "yellow", "red", "pink", "pale pink", "purple", "green", 
                    "blue", "orange", "none"]
bloom_season_opt = ["tbd", "Spring", "Summer", "Fall", "Winter", "None"]
pollinators_opt  = ["tbd", "Bees", "Butterflies", "Hummingbirds", "None"]
ca_native_opt    = ["tbd", "Yes", "No"]
ucd_all_star_opt = ["tbd", "Yes", "No"]
sun_exposure_opt = ["tbd", "Full Sun", "Partial Sun", "Partial Shade", "Full Shade"]
water_rqmts_opt  = ["tbd", "Very Low", "Low", "Medium", "High", "Very High"]
pH_opt           = ["tbd", 
                    "5.0", "5.1", "5.2", "5.3", "5.4", "5.5", "5.6", "5.7", "5.8", "5.9", 
                    "6.0", "6.1", "6.2", "6.3", "6.4", "6.5", "6.6", "6.7", "6.8", "6.9",
                    "7.0", "7.1", "7.2", "7.3", "7.4", "7.5", "7.6", "7.7", "7.8", "7.9",
                    "8.0"]
soil_type_opt    = ["tbd", "Sandy", "Loamy", "Clay"]
usda_zones_opt   = ["tbd", "1a", "1b",  "2a",  "2b",  "3a",  "3b", "4a", "4b",
                           "5a", "5b",  "6a",  "6b",  "7a",  "7b", "8a", "8b",
                           "9a", "9b", "10a", "10b", "11a", "11b"]
sunset_zones_opt = ["1A", "1B", "2A", "2B", "3A", "3B",  "4",  "5",  "6",  "7",  "8",  "9", "10", 
                    "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", 
                    "21", "22", "23", "24",
                    "A1", "A2", "A3", "H1", "H2"]
happiness_opt    = ["tbd", "Very Happy", "Happy", "Neutral", "Unhappy", "Very Unhappy"]
month_opt        = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def index(request):
    """ Render the landing page for Gateway Gardens app """
    return render(request, 'plants/index.html')

def gardens_summary(request):
    """ Render the individual user's garden summary for Gateway Gardens app """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    gardens = Garden.objects.all()
    template = loader.get_template("plants/gardens_summary.html")
    context = {}
    # AR: Only allow a user to have one garden defined
    my_gardens = 0
    all_gardens = 0
    for garden in gardens:
        if garden:
             all_gardens = all_gardens + 1
             if (request.user.username == garden.owner):
                context = { "garden" : garden }
                my_gardens = my_gardens + 1
        else:
            # no user has a garden in db
            return HttpResponseRedirect(reverse('plants:gardens_add')) 
    # current user has no gardens in db
    if my_gardens == 0:
        return HttpResponseRedirect(reverse('plants:gardens_add'))
    return HttpResponse(template.render(context, request))

def gardens_add(request):
    """ Add garden to the database """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
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

def gardens_update(request, id):
    """ Update garden details """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
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
 
def myplants_summary(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    
    # AR: Determine if this is really necessary
    template = loader.get_template("plants/myplants_summary.html")

    # Executed when search request is submitted
    if request.method == 'POST':
    
        # Get the search criteria from the "http request"
        # Plant Characteristics
        type_x_search           = request.POST["type_x_search"]
        bloom_color_search      = request.POST["bloom_color_search"]
        bloom_season_search     = request.POST["bloom_season_search"]
        bloom_month_search      = request.POST["bloom_month_search"]
        pollinators_search      = request.POST["pollinators_search"]
        ca_native_search        = request.POST["ca_native_search"]
        ucd_all_star_search     = request.POST["ucd_all_star_search"]
        # Plant Requirements
        sun_exposure_search     = request.POST["sun_exposure_search"]
        water_rqmts_search      = request.POST["water_rqmts_search"]
        soil_type_search        = request.POST["soil_type_search"]
        pH_search               = request.POST["pH_search"]
        usda_zone_search        = request.POST["usda_zone_search"]
        sunset_zone_search      = request.POST["sunset_zone_search"]
        # Garden Environment
        my_sun_exposure_search  = request.POST["my_sun_exposure_search"]
        my_water_level_search   = request.POST["my_water_level_search"]
        my_soil_type_search     = request.POST["my_soil_type_search"]
        my_happiness_search     = request.POST["my_happiness_search"]

        # Store the search criteria and get the previously stored column selections for the user
        gardens = Garden.objects.filter(owner = request.user.username)
        for garden in gardens:
            if (garden.owner == request.user.username):
                # Store the search criteria in the user's garden db table
                garden.type_x_search       = type_x_search
                garden.bloom_color_search  = bloom_color_search
                garden.bloom_season_search = bloom_season_search
                garden.bloom_month_search  = bloom_month_search
                garden.pollinators_search  = pollinators_search
                garden.ca_native_search    = ca_native_search
                garden.ucd_all_star_search = ucd_all_star_search
                garden.sun_exposure_search = sun_exposure_search
                garden.water_rqmts_search  = water_rqmts_search
                garden.pH_search           = pH_search
                garden.soil_type_search    = soil_type_search
                garden.usda_zone_search    = usda_zone_search
                garden.sunset_zone_search  = sunset_zone_search
                #
                garden.my_sun_exposure_search = my_sun_exposure_search
                garden.my_water_level_search  = my_water_level_search
                garden.my_soil_type_search    = my_soil_type_search
                garden.my_happiness_search    = my_happiness_search
                #
                garden.save()
                # Get the user's previously stored column display sections
                my_column_selection_list  = string2list(garden.column_selection)

        # Obtain the plants that the current user has claimed for their garden
        my_plants = MyPlant.objects.filter(owner = request.user.username)

        # Execute the search
        for my_plant in my_plants:
            # format multiselect attributes to remove [, ', and ]
            my_plant.plant.bloom_color  = string_display(my_plant.plant.bloom_color)
            my_plant.plant.bloom_season = string_display(my_plant.plant.bloom_season)
            my_plant.bloom_months       = string_display(my_plant.bloom_months)
            my_plant.plant.pollinators  = string_display(my_plant.plant.pollinators)
            my_plant.plant.sun_exposure = string_display(my_plant.plant.sun_exposure)
            my_plant.plant.water_rqmts  = string_display(my_plant.plant.water_rqmts)
            my_plant.plant.soil_type    = string_display(my_plant.plant.soil_type)
            # clean up the list display
            my_plant.sun_exposure = string_display(my_plant.sun_exposure)
            my_plant.water_level  = string_display(my_plant.water_level)
            my_plant.soil_type    = string_display(my_plant.soil_type)
            # Run through the search criteria to select the plants to show
            pH_hit = pH_check(pH_search, my_plant.plant.pH_min, my_plant.plant.pH_max)
            usda_zone_hit = usda_zone_check(usda_zone_search, my_plant.plant.usda_zone_min, my_plant.plant.usda_zone_max)
            sunset_zone_hit = sunset_zone_check(sunset_zone_search, my_plant.plant.sunset_zones, sunset_zones_opt)
            bloom_month_hit = bloom_month_check(bloom_month_search, my_plant.bloom_start, my_plant.bloom_end, month_opt)
            if  ( ( (type_x_search               == my_plant.plant.type_x)       or \
                    (type_x_search               == "Any")                       or \
                    (my_plant.plant.type_x       == "tbd")                          \
                  )                                                                 \
                  and                                                               \
                  ( (bloom_color_search          in my_plant.plant.bloom_color)  or \
                    (bloom_color_search          == "Any")                       or \
                    (my_plant.plant.bloom_color  == "tbd")                          \
                  )                                                                 \
                  and                                                               \
                  ( (bloom_season_search         in my_plant.plant.bloom_season) or \
                    (bloom_season_search         == "Any")                       or \
                    (my_plant.plant.bloom_season == "tbd")                          \
                  )                                                                 \
                  and                                                               \
                  ( (pollinators_search          in my_plant.plant.pollinators)  or \
                    (pollinators_search          == "Any")                       or \
                    (my_plant.plant.pollinators  == "tbd")                          \
                  )                                                                 \
                  and                                                               \
                  ( (ca_native_search             == my_plant.plant.ca_native)   or \
                    (ca_native_search             == "Any")                      or \
                    (my_plant.plant.ca_native     == "tbd")                         \
                   )                                                                \
                  and                                                               \
                  ( (ucd_all_star_search         == my_plant.plant.ucd_all_star) or \
                    (ucd_all_star_search         == "Any")                       or \
                    (my_plant.plant.ucd_all_star == "tbd")                          \
                  )                                                                 \
                  and                                                               \
                  ( (sun_exposure_search         in my_plant.plant.sun_exposure) or \
                    (sun_exposure_search         == "Any")                       or \
                    (my_plant.plant.sun_exposure == "tbd")                          \
                  )                                                                 \
                  and                                                               \
                  ( (water_rqmts_search         in my_plant.plant.water_rqmts)   or \
                    (water_rqmts_search         == "Any")                        or \
                    (my_plant.plant.water_rqmts == "tbd")                           \
                  )                                                                 \
                  and                                                               \
                  ( (soil_type_search            in my_plant.plant.soil_type)    or \
                    (soil_type_search            == "Any")                       or \
                    (my_plant.plant.soil_type    == "tbd")                          \
                  )                                                                 \
                  and                                                               \
                  ( pH_hit )                                                        \
                  and                                                               \
                  (usda_zone_hit)                                                   \
                  and                                                               \
                  (sunset_zone_hit)                                                 \
                  and                                                               \
                  (bloom_month_hit)                                                 \
                  and                                                               \
                  ( (my_sun_exposure_search      == my_plant.sun_exposure)       or \
                    (my_sun_exposure_search      == "Any")                       or \
                    (my_plant.sun_exposure       == "tbd")                          \
                  )                                                                 \
                  and                                                               \
                  ( (my_water_level_search      == my_plant.water_level)         or \
                    (my_water_level_search      == "Any")                        or \
                    (my_plant.water_level       == "tbd")                           \
                  )                                                                 \
                  and                                                               \
                  ( (my_soil_type_search         == my_plant.soil_type)          or \
                    (my_soil_type_search         == "Any")                       or \
                    (my_plant.soil_type          == "tbd")                          \
                  )                                                                 \
                  and                                                               \
                  ( (my_happiness_search         == my_plant.happiness)          or \
                    (my_happiness_search         == "Any")                       or \
                    (my_plant.happiness          == "tbd")                          \
                  )                                                                 \
                ):
                my_plant.show = "yes"
            else:
                my_plant.show = "no"

            gardens = Garden.objects.filter(owner = request.user.username)
            # Get the user's previously stored column display sections
            user_garden_found = False
            for garden in gardens:     
                # Get the user's previously stored column display sections  
                my_column_selection_list  = string2list(garden.my_column_selection)
                # Get the user's previously stored search criteria
                type_x_search         = garden.type_x_search
                bloom_color_search    = garden.bloom_color_search
                bloom_season_search   = garden.bloom_season_search
                bloom_month_search    = garden.bloom_month_search
                pollinators_search    = garden.pollinators_search
                ca_native_search      = garden.ca_native_search
                ucd_all_star_search   = garden.ucd_all_star_search
                sun_exposure_search   = garden.sun_exposure_search
                water_rqmts_search    = garden.water_rqmts_search
                pH_search             = garden.pH_search
                soil_type_search      = garden.soil_type_search
                usda_zone_search      = garden.usda_zone_search
                sunset_zone_search    = garden.sunset_zone_search
                #
                my_sun_exposure_search   = garden.my_sun_exposure_search
                my_water_level_search    = garden.my_water_level_search
                my_soil_type_search      = garden.my_soil_type_search
                my_happiness_search      = garden.my_happiness_search
                #
                user_garden_found     = True
                break # once the user's garden is found exit the loop

            # the current user needs to have a registered garden
            if (user_garden_found == False):
                return HttpResponseRedirect(reverse('plants:gardens_add'))

            context = { "my_plants"        : my_plants,
                        # search field options - plant attributes
                        "plant_types"      : plant_types,
                        "bloom_color_opt"  : bloom_color_opt,
                        "bloom_season_opt" : bloom_season_opt,
                        "pollinators_opt"  : pollinators_opt,
                        "ucd_all_star_opt" : ucd_all_star_opt,
                        "ca_native_opt"    : ca_native_opt,
                        # search field options - plant requirements & garden environment
                        "sun_exposure_opt" : sun_exposure_opt,
                        "water_rqmts_opt"  : water_rqmts_opt,
                        "soil_type_opt"    : soil_type_opt,
                        "pH_opt"           : pH_opt,
                        "usda_zones_opt"   : usda_zones_opt,
                        "sunset_zones_opt" : sunset_zones_opt,
                        "happiness_opt"    : happiness_opt,
                        "month_opt"        : month_opt,
                        
                        # search field defaults - plant attributes
                        "type_x_search"       : type_x_search,
                        "bloom_color_search"  : bloom_color_search,
                        "bloom_season_search" : bloom_season_search,
                        "bloom_month_search"  : bloom_month_search,
                        "pollinators_search"  : pollinators_search,
                        'ca_native_search'    : ca_native_search,
                        'ucd_all_star_search' : ucd_all_star_search,
                        # search field defaults - plant requirements
                        "sun_exposure_search" : sun_exposure_search,
                        "water_rqmts_search"  : water_rqmts_search,
                        "soil_type_search"    : soil_type_search,
                        "pH_search"           : pH_search,
                        "usda_zone_search"    : usda_zone_search,
                        "sunset_zone_search"  : sunset_zone_search,
                        # search field defaults - my plant conditions 
                        "my_sun_exposure_search" : my_sun_exposure_search,
                        "my_water_level_search"  : my_water_level_search,
                        "my_soil_type_search"    : my_soil_type_search,
                        "my_happiness_search"    : my_happiness_search,
                        # table column selection
                        "my_column_selection" : my_column_selection_list, 
                      }
            
        return render(request, "plants/myplants_summary.html", context)

    # Executed when plants summary page is initialized
    else:
        gardens = Garden.objects.filter(owner = request.user.username)
        # Get the user's previously stored column display sections
        user_garden_found = False
        for garden in gardens:
            if (garden.owner == request.user.username):
                # Get the user's previously stored column display sections
                column_selection_list  = string2list(garden.column_selection)
                # Get the user's previously stored search criteria
                type_x_search         = garden.type_x_search
                bloom_color_search    = garden.bloom_color_search
                bloom_season_search   = garden.bloom_season_search
                bloom_month_search    = garden.bloom_month_search
                pollinators_search    = garden.pollinators_search
                ca_native_search      = garden.ca_native_search
                ucd_all_star_search   = garden.ucd_all_star_search
                sun_exposure_search   = garden.sun_exposure_search
                water_rqmts_search    = garden.water_rqmts_search
                pH_search             = garden.pH_search
                soil_type_search      = garden.soil_type_search
                usda_zone_search      = garden.usda_zone_search
                sunset_zone_search    = garden.sunset_zone_search

                my_sun_exposure_search   = garden.my_sun_exposure_search
                my_water_level_search    = garden.my_water_level_search
                my_soil_type_search      = garden.my_soil_type_search
                my_happiness_search      = garden.my_happiness_search

                user_garden_found     = True
                break # once the user's garden is found exit the loop

        # the current user needs to have a registered garden
        if (user_garden_found == False):
            return HttpResponseRedirect(reverse('plants:gardens_add'))

        # Obtain the plants that the current user has claimed for their garden
        my_plants = MyPlant.objects.filter(owner = request.user.username)

        # Execute the search
        for my_plant in my_plants:
            # format multiselect attributes to remove [, ', and ]
            my_plant.plant.bloom_color  = string_display(my_plant.plant.bloom_color)
            my_plant.plant.bloom_season = string_display(my_plant.plant.bloom_season)
            my_plant.bloom_months       = string_display(my_plant.plant.bloom_months)
            my_plant.plant.pollinators  = string_display(my_plant.plant.pollinators)
            my_plant.plant.sun_exposure = string_display(my_plant.plant.sun_exposure)
            my_plant.plant.water_rqmts  = string_display(my_plant.plant.water_rqmts)
            my_plant.plant.soil_type    = string_display(my_plant.plant.soil_type)
            # clean up the list display
            my_plant.sun_exposure = string_display(my_plant.sun_exposure)
            my_plant.water_level  = string_display(my_plant.water_level)
            my_plant.soil_type    = string_display(my_plant.soil_type)
            # Run through the search criteria to select the plants to show
            pH_hit = pH_check(pH_search, my_plant.plant.pH_min, my_plant.plant.pH_max)
            usda_zone_hit = usda_zone_check(usda_zone_search, my_plant.plant.usda_zone_min, my_plant.plant.usda_zone_max)
            sunset_zone_hit = sunset_zone_check(sunset_zone_search, my_plant.plant.sunset_zones, sunset_zones_opt)
            bloom_month_hit = bloom_month_check(bloom_month_search, my_plant.bloom_start, my_plant.bloom_end, month_opt)
            if  ( ( (type_x_search               == my_plant.plant.type_x)       or \
                    (type_x_search               == "Any")                       or \
                    (my_plant.plant.type_x       == "tbd")                          \
                  )                                                                 \
                  and                                                               \
                  ( (bloom_color_search          in my_plant.plant.bloom_color)  or \
                    (bloom_color_search          == "Any")                       or \
                    (my_plant.plant.bloom_color  == "tbd")                          \
                  )                                                                 \
                  and                                                               \
                  ( (bloom_season_search         in my_plant.plant.bloom_season) or \
                    (bloom_season_search         == "Any")                       or \
                    (my_plant.plant.bloom_season == "tbd")                          \
                  )                                                                 \
                  and                                                               \
                  ( (pollinators_search          in my_plant.plant.pollinators)  or \
                    (pollinators_search          == "Any")                       or \
                    (my_plant.plant.pollinators  == "tbd")                          \
                  )                                                                 \
                  and                                                               \
                  ( (ca_native_search             == my_plant.plant.ca_native)   or \
                    (ca_native_search             == "Any")                      or \
                    (my_plant.plant.ca_native     == "tbd")                         \
                   )                                                                \
                  and                                                               \
                  ( (ucd_all_star_search         == my_plant.plant.ucd_all_star) or \
                    (ucd_all_star_search         == "Any")                       or \
                    (my_plant.plant.ucd_all_star == "tbd")                          \
                  )                                                                 \
                  and                                                               \
                  ( (sun_exposure_search         in my_plant.plant.sun_exposure) or \
                    (sun_exposure_search         == "Any")                       or \
                    (my_plant.plant.sun_exposure == "tbd")                          \
                  )                                                                 \
                  and                                                               \
                  ( (water_rqmts_search         in my_plant.plant.water_rqmts)   or \
                    (water_rqmts_search         == "Any")                        or \
                    (my_plant.plant.water_rqmts == "tbd")                           \
                  )                                                                 \
                  and                                                               \
                  ( (soil_type_search            in my_plant.plant.soil_type)    or \
                    (soil_type_search            == "Any")                       or \
                    (my_plant.plant.soil_type    == "tbd")                          \
                  )                                                                 \
                  and                                                               \
                  ( pH_hit )                                                        \
                  and                                                               \
                  (usda_zone_hit)                                                   \
                  and                                                               \
                  (sunset_zone_hit)                                                 \
                  and                                                               \
                  (bloom_month_hit)                                                 \
                  and                                                               \
                  ( (my_sun_exposure_search      == my_plant.sun_exposure)       or \
                    (my_sun_exposure_search      == "Any")                       or \
                    (my_plant.sun_exposure       == "tbd")                          \
                  )                                                                 \
                  and                                                               \
                  ( (my_water_level_search      == my_plant.water_level)         or \
                    (my_water_level_search      == "Any")                        or \
                    (my_plant.water_level       == "tbd")                           \
                  )                                                                 \
                  and                                                               \
                  ( (my_soil_type_search         == my_plant.soil_type)          or \
                    (my_soil_type_search         == "Any")                       or \
                    (my_plant.soil_type          == "tbd")                          \
                  )                                                                 \
                  and                                                               \
                  ( (my_happiness_search         == my_plant.happiness)          or \
                    (my_happiness_search         == "Any")                       or \
                    (my_plant.happiness          == "tbd")                          \
                  )                                                                 \
                ):
                my_plant.show = "yes"
            else:
                my_plant.show = "no"

        gardens = Garden.objects.filter(owner = request.user.username)
        # Get the user's previously stored column display sections
        for garden in gardens:       
            my_column_selection_list  = string2list(garden.my_column_selection)
        context = { 'my_plants'           : my_plants,
                    # search field options - plant attributes
                    "plant_types"      : plant_types,
                    "bloom_color_opt"  : bloom_color_opt,
                    "bloom_season_opt" : bloom_season_opt,
                    "pollinators_opt"  : pollinators_opt,
                    "ucd_all_star_opt" : ucd_all_star_opt,
                    "ca_native_opt"    : ca_native_opt,
                    # search field options - plant requirements & garden environment
                    "sun_exposure_opt" : sun_exposure_opt,
                    "water_rqmts_opt"  : water_rqmts_opt,
                    "soil_type_opt"    : soil_type_opt,
                    "pH_opt"           : pH_opt,
                    "usda_zones_opt"   : usda_zones_opt,
                    "sunset_zones_opt" : sunset_zones_opt,
                    "happiness_opt"    : happiness_opt,
                    "month_opt"        : month_opt,
                    # search field defaults - plant attributes
                    "type_x_search"       : type_x_search,
                    "bloom_color_search"  : bloom_color_search,
                    "bloom_season_search" : bloom_season_search,
                    "bloom_month_search"  : bloom_month_search,
                    "pollinators_search"  : pollinators_search,
                    'ca_native_search'    : ca_native_search,
                    'ucd_all_star_search' : ucd_all_star_search,
                    # search field defaults - plant requirements
                    "sun_exposure_search" : sun_exposure_search,
                    "water_rqmts_search"  : water_rqmts_search,
                    "soil_type_search"    : soil_type_search,
                    "pH_search"           : pH_search,
                    "usda_zone_search"    : usda_zone_search,
                    "sunset_zone_search"  : sunset_zone_search,
                    # search field defaults - my plant conditions
                    "my_sun_exposure_search" : my_sun_exposure_search,
                    "my_water_level_search"  : my_water_level_search,
                    "my_soil_type_search"    : my_soil_type_search,
                    "my_happiness_search"    : my_happiness_search,
                    # table column selection
                    'my_column_selection' : my_column_selection_list, }
        return HttpResponse(template.render(context, request))

def myplants_add(request, id):
    """ Associate a 'plant' to 'my_plant' """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    plant = Plant.objects.get(id=id)
    my_plant = MyPlant()
    if request.POST:
        form = MyPlantAddUpdateForm(request.POST)
        if form.is_valid():
            my_plant.owner        = request.user.username                 #
            my_plant.date_planted = form.cleaned_data.get("date_planted") #
            my_plant.location     = form.cleaned_data.get("location")     #
            my_plant.sun_exposure = form.cleaned_data.get("sun_exposure") #
            my_plant.water_level  = form.cleaned_data.get("water_level")  #
            my_plant.soil_type    = form.cleaned_data.get("soil_type")    #
            my_plant.pH           = form.cleaned_data.get("pH")           #
            my_plant.bloom_color  = form.cleaned_data.get("bloom_color")  #
            my_plant.bloom_start  = form.cleaned_data.get("bloom_start")  #
            my_plant.bloom_end    = form.cleaned_data.get("bloom_end")    #
            my_plant.happiness    = form.cleaned_data.get("happiness")    #
            my_plant.notes        = form.cleaned_data.get("notes")        #
            my_plant.plant        = plant                                 # link my_plant to the specific plant
            # Build list of bloom months
            my_plant.bloom_months = bloom_month_list(my_plant.bloom_start, my_plant.bloom_end, month_opt)   
            my_plant.save()
        return HttpResponseRedirect(reverse('plants:plants_summary')) 
    else:
        form = MyPlantAddUpdateForm()
        context = { 'form' : form }
        return render(request, 'plants/myplants_add.html', context)
    
def myplants_update(request, id):
    """ Update details related a specific My Plant """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    my_plant = MyPlant.objects.get(id=id)
    if request.POST:
        form = MyPlantAddUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            my_plant.date_planted = form.cleaned_data.get("date_planted") #
            my_plant.location     = form.cleaned_data.get("location")     #
            my_plant.sun_exposure = form.cleaned_data.get("sun_exposure") #
            my_plant.water_level  = form.cleaned_data.get("water_level")  #
            my_plant.soil_type    = form.cleaned_data.get("soil_type")    #
            my_plant.pH           = form.cleaned_data.get("pH")           #
            my_plant.bloom_color  = form.cleaned_data.get("bloom_color")  #
            my_plant.bloom_start  = form.cleaned_data.get("bloom_start")  #
            my_plant.bloom_end    = form.cleaned_data.get("bloom_end")    #
            my_plant.happiness    = form.cleaned_data.get("happiness")    #
            my_plant.notes        = form.cleaned_data.get("notes")        #
            # Build list of bloom months
            my_plant.bloom_months = bloom_month_list(my_plant.bloom_start, my_plant.bloom_end, month_opt)   
            my_plant.save()
        return HttpResponseRedirect(reverse('plants:myplants_summary')) 
    else:
        # convert string-based lists (retrieved from db) to true Python lists
        sun_exposure_list = string2list(my_plant.sun_exposure)
        water_level_list = string2list(my_plant.water_level)
        # set the update form with the current db values
        form = MyPlantAddUpdateForm(initial={ 'date_planted' : my_plant.date_planted,
                                              'location'     : my_plant.location,
                                              'sun_exposure' : sun_exposure_list,
                                              'water_level'  : water_level_list,
                                              'soil_type'    : my_plant.soil_type,
                                              'pH'           : my_plant.pH,
                                              'bloom_color'  : my_plant.bloom_color,
                                              'bloom_start'  : my_plant.bloom_start,
                                              'bloom_end'    : my_plant.bloom_end,
                                              'happiness'    : my_plant.happiness,
                                              'notes'        : my_plant.notes,
                                            })
        context = { 'form' : form }
        return render(request, 'plants/myplants_update.html', context)

def myplants_delete(request, id):
    """ Delete selected plant from the MyPlants database table """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    myplant = MyPlant.objects.get(id=id)
    if request.POST:
        myplant.delete()
        return HttpResponseRedirect(reverse('plants:myplants_summary')) 
    else:
        context = {'myplant': myplant}
        return render(request, 'plants/myplants_delete_modal.html', context)

def myplants_remove(request, id):
    """ Remove selected plant from the MyPlants database  """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    #
    plant = Plant.objects.get(id=id)
    if request.POST:
        my_plants = MyPlant.objects.filter(owner = request.user.username) 
        for my_plant in my_plants:
            if my_plant.plant == plant:
                my_plant.delete()
        return HttpResponseRedirect(reverse('plants:plants_summary')) 
    else:
        context = { 'plant' : plant }
        return render(request, 'plants/myplants_remove_modal.html', context)

def myplants_details(request, id):
    """ Show a detailed view of a specific plant """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    # Uses the id to locate the correct record in the MyPlant table
    my_plant = MyPlant.objects.get(id=id)
    # format multiselect attributes to remove [, ', and ]
    my_plant.sun_exposure = string_display(my_plant.sun_exposure)
    plant   = Plant.objects.get(id=my_plant.plant.id)
    # format multiselect attributes to remove [, ', and ] 
    plant.bloom_color  = string_display(plant.bloom_color)
    plant.bloom_season = string_display(plant.bloom_season)
    plant.pollinators  = string_display(plant.pollinators)
    plant.sun_exposure = string_display(plant.sun_exposure)
    plant.water_rqmts  = string_display(plant.water_rqmts)
    plant.soil_type    = string_display(plant.soil_type)
    # get all comments related to the plant                
    myplant_comments = MyPlantComment.objects.filter(myplant__pk=id) 
    template = loader.get_template("plants/myplants_details.html")
    context  = { "my_plant"          : my_plant, 
                 "plant"            : plant,
                 "myplant_comments" : myplant_comments, 
               }
    # Send "context" to template and output the html from the template
    return HttpResponse(template.render(context, request)) 

def myplants_comment(request, id):
    """ Associate a comment to a myplant """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    myplant = MyPlant.objects.get(id=id)
    my_plant_comment = MyPlantComment()
    if request.POST:
        form = MyPlantCommentForm(request.POST, request.FILES)
        if form.is_valid():
            my_plant_comment.author  = request.user.username            #
            my_plant_comment.subject = form.cleaned_data.get("subject") #
            my_plant_comment.comment = form.cleaned_data.get("comment") #
            my_plant_comment.myplant = myplant                          # link the comment to the specific plant
            my_plant_comment.save()
        return HttpResponseRedirect(reverse('plants:myplants_details', args=(myplant.id,))) 
    else:
        form = MyPlantCommentForm()
        context = { 'myplant' : myplant,
                    'form'    : form,
                  }
        return render(request, 'plants/myplants_comment.html', context)

def plants_summary(request):
    """ Render the Searchable summary list of plants with comments for Gateway Gardens app """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    
    # Executed when search request is submitted
    if request.method == 'POST':   
        template = loader.get_template("plants/plants_summary.html")

        # Get the search criteria from the "http request"
        # Plant Characteristics
        type_x_search        = request.POST["type_x_search"]
        bloom_color_search   = request.POST["bloom_color_search"]
        bloom_season_search  = request.POST["bloom_season_search"]
        bloom_month_search   = request.POST["bloom_month_search"]
        pollinators_search   = request.POST["pollinators_search"]
        ca_native_search     = request.POST["ca_native_search"]
        ucd_all_star_search  = request.POST["ucd_all_star_search"]
        # Plant Requirements
        sun_exposure_search  = request.POST["sun_exposure_search"]
        water_rqmts_search   = request.POST["water_rqmts_search"]
        pH_search            = request.POST["pH_search"]
        soil_type_search     = request.POST["soil_type_search"]
        usda_zone_search     = request.POST["usda_zone_search"]
        sunset_zone_search   = request.POST["sunset_zone_search"]
        garden_search        = request.POST["garden_search"]

        # Store the search criteria and get the previously stored column selections for the user
        gardens = Garden.objects.filter(owner = request.user.username)
        for garden in gardens:
            if (garden.owner == request.user.username):
                # Store the search criteria in the user's garden db table
                garden.type_x_search       = type_x_search
                garden.bloom_color_search  = bloom_color_search
                garden.bloom_season_search = bloom_season_search
                garden.bloom_month_search  = bloom_month_search
                garden.pollinators_search  = pollinators_search
                garden.ca_native_search    = ca_native_search
                garden.ucd_all_star_search = ucd_all_star_search
                garden.sun_exposure_search = sun_exposure_search
                garden.water_rqmts_search  = water_rqmts_search
                garden.pH_search           = pH_search
                garden.soil_type_search    = soil_type_search
                garden.usda_zone_search    = usda_zone_search
                garden.sunset_zone_search  = sunset_zone_search
                garden.garden_search       = garden_search
                garden.save()
                # Get the user's previously stored column display sections
                column_selection_list  = string2list(garden.column_selection)

        # Obtain the plants that the current user has claimed for their garden - needed to populate the table
        my_plants = MyPlant.objects.filter(owner = request.user.username) 

        # Plant query -> Plants claimed by the current user or all plants in the database
        if garden_search == "Mine":
            plants = Plant.objects.filter(myplants__owner = request.user.username) 
        else:
            plants = Plant.objects.all()

        # Run through the search criteria to select the plants to show
        for plant in plants:
            # Run through the search criteria to select the plants to show
            pH_hit = pH_check(pH_search, plant.pH_min, plant.pH_max)
            usda_zone_hit = usda_zone_check(usda_zone_search, plant.usda_zone_min, plant.usda_zone_max)
            sunset_zone_hit = sunset_zone_check(sunset_zone_search, plant.sunset_zones, sunset_zones_opt)
            bloom_month_hit = bloom_month_check(bloom_month_search, plant.bloom_start, plant.bloom_end, month_opt)
            if ((type_x_search       == plant.type_x)       or (type_x_search       == "Any") or (plant.type_x       == "tbd")) and \
               ((bloom_color_search  in plant.bloom_color)  or (bloom_color_search  == "Any") or (plant.bloom_color  == "tbd")) and \
               ((bloom_season_search in plant.bloom_season) or (bloom_season_search == "Any") or (plant.bloom_season == "tbd")) and \
               ((pollinators_search  in plant.pollinators)  or (pollinators_search  == "Any") or (plant.pollinators  == "tbd")) and \
               ((ca_native_search    == plant.ca_native)    or (ca_native_search    == "Any") or (plant.ca_native    == "tbd")) and \
               ((ucd_all_star_search == plant.ucd_all_star) or (ucd_all_star_search == "Any") or (plant.ucd_all_star == "tbd")) and \
               ((sun_exposure_search in plant.sun_exposure) or (sun_exposure_search == "Any") or (plant.sun_exposure == "tbd")) and \
               ((water_rqmts_search  == plant.water_rqmts)  or (water_rqmts_search  == "Any") or (plant.water_rqmts  == "tbd")) and \
               ((soil_type_search in plant.soil_type) or (soil_type_search == "Any") or (plant.soil_type  == "tbd")) and \
               (pH_hit) and \
               (usda_zone_hit) and \
               (sunset_zone_hit) and \
               (bloom_month_hit):
                # show selected plant
                plant.plant_show = "yes"
            else:
                plant.plant_show = "no"

            # Save the plant show flag to the database
            plant.save()
            # format multiselect attributes to remove [, ', and ]
            plant.bloom_color  = string_display(plant.bloom_color)
            plant.bloom_season = string_display(plant.bloom_season)
            plant.pollinators  = string_display(plant.pollinators)
            plant.sun_exposure = string_display(plant.sun_exposure)
            plant.water_rqmts  = string_display(plant.water_rqmts)
            plant.soil_type    = string_display(plant.soil_type)
            # check to determine if the current user has claimed the plant
            for my_plant in my_plants:
                if my_plant.plant == plant:
                    plant.plant_mine = "yes"
                    break # Found the plant in my plants
                else:
                    plant.plant_mine = "no"
        # Send selected plant details to template
        context = { "plants"             : plants,
                    # Search attributes
                    'plant_types'        : plant_types,
                    "bloom_color_opt"    : bloom_color_opt,
                    "bloom_season_opt"   : bloom_season_opt,
                    "pollinators_opt"    : pollinators_opt,
                    "ucd_all_star_opt"   : ucd_all_star_opt,
                    "ca_native_opt"      : ca_native_opt,
                    "sun_exposure_opt"   : sun_exposure_opt,
                    "water_rqmts_opt"    : water_rqmts_opt,
                    "pH_opt"             : pH_opt,
                    "soil_type_opt"      : soil_type_opt,
                    "usda_zones_opt"     : usda_zones_opt,
                    "sunset_zones_opt"   : sunset_zones_opt,
                    "month_opt"          : month_opt,
                    # Search option values from previous search if applicable else default of "Any"
                    "type_x_search"       : type_x_search,
                    "bloom_color_search"  : bloom_color_search,
                    "bloom_season_search" : bloom_season_search,
                    "bloom_month_search"  : bloom_month_search,
                    'pollinators_search'  : pollinators_search,
                    'ca_native_search'    : ca_native_search,
                    'ucd_all_star_search' : ucd_all_star_search,
                    "sun_exposure_search" : sun_exposure_search,
                    "water_rqmts_search"  : water_rqmts_search,
                    "pH_search"           : pH_search,
                    "soil_type_search"    : soil_type_search,
                    "usda_zone_search"    : usda_zone_search,
                    "sunset_zone_search"  : sunset_zone_search,
                    'garden_search'       : garden_search,
                    # table column selection
                    'column_selection'   : column_selection_list,
                  }
        return render(request, "plants/plants_summary.html", context)
    # Executed when plants summary page is initialized
    else:
        gardens = Garden.objects.filter(owner = request.user.username)
        # Get the user's previously stored column display sections
        user_garden_found = False
        for garden in gardens:
            if (garden.owner == request.user.username):
                # Get the user's previously stored column display sections
                column_selection_list  = string2list(garden.column_selection)
                # Get the user's previously stored search criteria
                type_x_search         = garden.type_x_search
                bloom_color_search    = garden.bloom_color_search
                bloom_season_search   = garden.bloom_season_search
                bloom_month_search    = garden.bloom_month_search
                pollinators_search    = garden.pollinators_search
                ca_native_search      = garden.ca_native_search
                ucd_all_star_search   = garden.ucd_all_star_search
                sun_exposure_search   = garden.sun_exposure_search
                water_rqmts_search    = garden.water_rqmts_search
                pH_search             = garden.pH_search
                soil_type_search      = garden.soil_type_search
                usda_zone_search      = garden.usda_zone_search
                sunset_zone_search    = garden.sunset_zone_search
                garden_search         = garden.garden_search
                user_garden_found     = True
                break # once the user's garden is found exit the loop

        # the current user needs to have a registered garden
        if (user_garden_found == False):
            return HttpResponseRedirect(reverse('plants:gardens_add'))
        
        # Obtain the plants that the current user has claimed for their garden
        my_plants = MyPlant.objects.filter(owner = request.user.username) 
        # Execute the search
        plants   = Plant.objects.all()
        for plant in plants:
            # Run through the search criteria to select the plants to show
            pH_hit = pH_check(pH_search, plant.pH_min, plant.pH_max)
            usda_zone_hit = usda_zone_check(usda_zone_search, plant.usda_zone_min, plant.usda_zone_max)
            sunset_zone_hit = sunset_zone_check(sunset_zone_search, plant.sunset_zones, sunset_zones_opt)
            bloom_month_hit = bloom_month_check(bloom_month_search, plant.bloom_start, plant.bloom_end, month_opt)
            if  ((type_x_search       == plant.type_x)       or (type_x_search       == "Any") or (plant.type_x       == "tbd")) and \
                ((bloom_color_search  in plant.bloom_color)  or (bloom_color_search  == "Any") or (plant.bloom_color  == "tbd")) and \
                ((bloom_season_search in plant.bloom_season) or (bloom_season_search == "Any") or (plant.bloom_season == "tbd")) and \
                ((pollinators_search  in plant.pollinators)  or (pollinators_search  == "Any") or (plant.pollinators  == "tbd")) and \
                ((ca_native_search    == plant.ca_native)    or (ca_native_search    == "Any") or (plant.ca_native    == "tbd")) and \
                ((ucd_all_star_search == plant.ucd_all_star) or (ucd_all_star_search == "Any") or (plant.ucd_all_star == "tbd")) and \
                ((sun_exposure_search in plant.sun_exposure) or (sun_exposure_search == "Any") or (plant.sun_exposure == "tbd")) and \
                ((water_rqmts_search  == plant.water_rqmts)  or (water_rqmts_search  == "Any") or (plant.water_rqmts  == "tbd")) and \
                ((soil_type_search    in plant.soil_type)    or (soil_type_search    == "Any") or (plant.soil_type    == "tbd")) and \
                (pH_hit) and \
                (usda_zone_hit) and \
                (sunset_zone_hit) and \
                (bloom_month_hit):
                # show selected plant
                plant.plant_show = "yes"
            else:
                plant.plant_show = "no"

            # Save the plant show flag to the database
            plant.save()

            # format multiselect attributes to remove [, ', and ]
            plant.bloom_color  = string_display(plant.bloom_color)
            plant.bloom_season = string_display(plant.bloom_season)
            plant.bloom_months = string_display(plant.bloom_months)
            plant.pollinators  = string_display(plant.pollinators)
            plant.sun_exposure = string_display(plant.sun_exposure)
            plant.water_rqmts  = string_display(plant.water_rqmts)
            plant.soil_type    = string_display(plant.soil_type)
            # Check to see if the current user has claimed the plant
            for my_plant in my_plants:
                if my_plant.plant == plant:
                    plant.plant_mine = "yes"
                    break # Found the plant in my plants
                else:
                    plant.plant_mine = "no"

        # Send selected plant details to template
        template = loader.get_template("plants/plants_summary.html")
        context = { "plants"             : plants,
                    "my_plants"          : my_plants,
                    # search field options
                    "plant_types"        : plant_types,
                    "bloom_color_opt"    : bloom_color_opt,
                    "bloom_season_opt"   : bloom_season_opt,
                    "pollinators_opt"    : pollinators_opt,
                    "ca_native_opt"      : ca_native_opt,
                    "ucd_all_star_opt"   : ucd_all_star_opt,
                    "sun_exposure_opt"   : sun_exposure_opt,
                    "water_rqmts_opt"    : water_rqmts_opt,
                    "pH_opt"             : pH_opt,
                    "soil_type_opt"      : soil_type_opt,
                    "usda_zones_opt"     : usda_zones_opt,
                    "sunset_zones_opt"   : sunset_zones_opt,
                    "month_opt"          : month_opt,
                    # search field defaults
                    "type_x_search"       : type_x_search,
                    "bloom_color_search"  : bloom_color_search,
                    "bloom_season_search" : bloom_season_search,
                    "bloom_month_search"  : bloom_month_search,
                    "pollinators_search"  : pollinators_search,
                    'ca_native_search'    : ca_native_search,
                    'ucd_all_star_search' : ucd_all_star_search,
                    "sun_exposure_search" : sun_exposure_search,
                    "water_rqmts_search"  : water_rqmts_search,
                    "soil_type_search"    : soil_type_search,
                    "pH_search"           : pH_search,
                    "usda_zone_search"    : usda_zone_search,
                    "sunset_zone_search"  : sunset_zone_search,
                    'garden_search'       : garden_search,
                    # table column selection
                    'column_selection'   : column_selection_list,
              }
        
    return HttpResponse(template.render(context, request))

def plants_chart(request):
    """ Create a table for the selected plants on a month-by-month basis """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    plants = Plant.objects.all()
    context = { 'plants' : plants }
    return render(request, 'plants/plants_chart_modal.html', context)

def plants_details(request, id):
    """ Show a detailed view of a specific plant """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    plant = Plant.objects.get(id=id)                     # Uses the id to locate the correct record in the Plant table
    comments = Comment.objects.filter(plant__pk=id)      # get all comments related to the plant
    # format multiselect attributes to remove [, ', and ]
    plant.sun_exposure = string_display(plant.sun_exposure)
    plant.water_rqmts  = string_display(plant.water_rqmts)
    plant.bloom_color  = string_display(plant.bloom_color)
    plant.bloom_season = string_display(plant.bloom_season)
    plant.pollinators  = string_display(plant.pollinators)
    plant.soil_type    = string_display(plant.soil_type)

    if (plant.height_inch != 0):
        height_adj = plant.height_feet + (plant.height_inch / 12)
        plant.height_feet = math.floor(height_adj)
        plant.height_inch = plant.height_inch%12
    if (plant.width_inch != 0):
        width_adj = plant.width_feet + (plant.width_inch / 12)
        plant.width_feet = math.floor(width_adj)
        plant.width_inch = plant.width_inch%12
    template = loader.get_template("plants/plants_details.html")  # loads the plant_details.html template
    # Get the pests associated with this plant & sort by pest name
    pests = Pest.objects.filter(plants__id=plant.id).order_by('pest_name')
    context = { "plant"    : plant, 
                "pests"    : pests,    
                "comments" : comments, 
            }
    return HttpResponse(template.render(context, request)) # Send "context" to template and output the html from the template

def plants_add(request):
    """ Render the page to add plants to the database for Gateway Gardens app """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    plant = Plant()
    if request.POST:
        form = PlantAddUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            plant.commonName    = form.cleaned_data.get('commonName')
            plant.type_x        = form.cleaned_data.get('type_x')
            plant.bloom_color   = form.cleaned_data.get('bloom_color')
            plant.bloom_season  = form.cleaned_data.get('bloom_season')
            plant.bloom_start   = form.cleaned_data.get('bloom_start')
            plant.bloom_end     = form.cleaned_data.get('bloom_end')
            plant.pollinators   = form.cleaned_data.get('pollinators')
            plant.height_feet   = form.cleaned_data.get('height_feet')
            plant.height_inch   = form.cleaned_data.get('height_inch')
            plant.width_feet    = form.cleaned_data.get('width_feet')
            plant.width_inch    = form.cleaned_data.get('width_inch')
            plant.sun_exposure  = form.cleaned_data.get('sun_exposure')
            plant.water_rqmts   = form.cleaned_data.get('water_rqmts')
            plant.pH_min        = form.cleaned_data.get('pH_min')
            plant.pH_max        = form.cleaned_data.get('pH_max')
            plant.soil_type     = form.cleaned_data.get("soil_type")
            plant.ucd_all_star  = form.cleaned_data.get('ucd_all_star')
            plant.ca_native     = form.cleaned_data.get('ca_native')
            plant.usda_zone_min = form.cleaned_data.get('usda_zone_min')
            plant.usda_zone_max = form.cleaned_data.get('usda_zone_max')
            plant.sunset_zones  = form.cleaned_data.get('sunset_zones')
            plant.kingdom       = form.cleaned_data.get('kingdom')
            plant.subkingdom    = form.cleaned_data.get('subkingdom')
            plant.superdivision = form.cleaned_data.get('superdivision')
            plant.division      = form.cleaned_data.get('division')
            plant.class_x       = form.cleaned_data.get('class_x')
            plant.subclass      = form.cleaned_data.get('subclass')
            plant.order         = form.cleaned_data.get('order')
            plant.family        = form.cleaned_data.get('family')
            plant.genus         = form.cleaned_data.get('genus')
            plant.species       = form.cleaned_data.get('species')
            plant.variety       = form.cleaned_data.get('variety')
            plant.phonetic_spelling = form.cleaned_data.get('phonetic_spelling')
            if 'blob' in request.FILES:
                audio_name = request.FILES['blob']
                plant.audio_name = audio_name
            plant.description    = form.cleaned_data.get('description')
            plant.pruning        = form.cleaned_data.get('pruning')
            plant.fertilization  = form.cleaned_data.get('fertilization')
            plant.propagation    = form.cleaned_data.get('propagation')
            plant.pests_diseases = form.cleaned_data.get('pests_diseases')
            # Check to see if an image file has been specified
            if 'image_1' in request.FILES:
                plant.image_1   = request.FILES['image_1']
                plant.caption_1 = form.cleaned_data.get('caption_1')
            if 'image_2' in request.FILES:
                plant.image_2   = request.FILES['image_2']
                plant.caption_2 = form.cleaned_data.get('caption_2')
            if 'image_3' in request.FILES:
                plant.image_3   = request.FILES['image_3']
                plant.caption_3 = form.cleaned_data.get('caption_3')
            if 'image_4' in request.FILES:
                plant.image_4   = request.FILES['image_4']
                plant.caption_4 = form.cleaned_data.get('caption_4')
            plant.creator       = request.user.username
            plant.creator_notes = form.cleaned_data.get('creator_notes')
            # Build list of bloom months
            plant.bloom_months = bloom_month_list(plant.bloom_start, plant.bloom_end, month_opt) 
            plant.save()

            # Add the selected pests to the selected plant
            pest_list = request.POST.getlist('pest_list')
            pests = Pest.objects.all()
            for pest_item in pest_list:
                for pest in pests:
                    if (pest.pest_name == pest_item):
                        print("DEBUG: pest_name =", pest.pest_name)
                        pest.plants.add(plant)

        return HttpResponseRedirect(reverse('plants:plants_summary'))
    else:
        form = PlantAddUpdateForm()
        pests = Pest.objects.all()
        context = { 'form'             : form,
                    'pests'            : pests,
                    'usda_zones_opt'   : usda_zones_opt,
                    'sunset_zones_opt' : sunset_zones_opt }
        return render(request, 'plants/plants_add.html', context)

def plants_update(request, id):
    """ Update the attributes for an existing plant """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    plant = Plant.objects.get(id=id)
    if request.POST:
        form = PlantAddUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            plant.commonName    = form.cleaned_data.get('commonName')
            plant.type_x        = form.cleaned_data.get('type_x')
            plant.bloom_color   = form.cleaned_data.get('bloom_color')
            plant.bloom_season  = form.cleaned_data.get('bloom_season')
            plant.bloom_start   = form.cleaned_data.get('bloom_start')
            plant.bloom_end     = form.cleaned_data.get('bloom_end')
            plant.height_feet   = form.cleaned_data.get('height_feet')
            plant.height_inch   = form.cleaned_data.get('height_inch')
            plant.width_feet    = form.cleaned_data.get('width_feet')
            plant.width_inch    = form.cleaned_data.get('width_inch')
            plant.pollinators   = form.cleaned_data.get('pollinators')
            plant.ca_native     = form.cleaned_data.get('ca_native')
            plant.ucd_all_star  = form.cleaned_data.get('ucd_all_star')
            plant.sun_exposure  = form.cleaned_data.get('sun_exposure')
            plant.water_rqmts   = form.cleaned_data.get('water_rqmts')
            plant.pH_min        = form.cleaned_data.get('pH_min')
            plant.pH_max        = form.cleaned_data.get('pH_max')
            plant.soil_type     = form.cleaned_data.get('soil_type')
            plant.usda_zone_min = form.cleaned_data.get('usda_zone_min')
            plant.usda_zone_max = form.cleaned_data.get('usda_zone_max')
            plant.sunset_zones  = form.cleaned_data.get('sunset_zones')
            plant.kingdom       = form.cleaned_data.get('kingdom')
            plant.subkingdom    = form.cleaned_data.get('subkingdom')
            plant.superdivision = form.cleaned_data.get('superdivision')
            plant.division      = form.cleaned_data.get('division')
            plant.class_x       = form.cleaned_data.get('class_x')
            plant.subclass      = form.cleaned_data.get('subclass')
            plant.order         = form.cleaned_data.get('order')
            plant.family        = form.cleaned_data.get('family')
            plant.genus         = form.cleaned_data.get('genus')
            plant.species       = form.cleaned_data.get('species')
            plant.variety       = form.cleaned_data.get('variety')
            plant.phonetic_spelling = form.cleaned_data.get('phonetic_spelling')
            if 'blob' in request.FILES:
                if (plant.audio_name):
                    os.remove(plant.audio_name.path)
                plant.audio_name = request.FILES['blob']
            plant.description    = form.cleaned_data.get('description')
            plant.pruning        = form.cleaned_data.get('pruning')
            plant.fertilization  = form.cleaned_data.get('fertilization')
            plant.propagation    = form.cleaned_data.get('propagation')
            plant.pests_diseases = form.cleaned_data.get('pests_diseases')
            # Process images - check for new image - if yes, delete any existing image
            if 'image_1' in request.FILES:
                if (plant.image_1):
                    os.remove(plant.image_1.path)
                plant.image_1 = request.FILES['image_1']
            plant.caption_1 = form.cleaned_data.get('caption_1')
            
            if 'image_2' in request.FILES:
                if (plant.image_2):
                    os.remove(plant.image_2.path)
                plant.image_2 = request.FILES['image_2']
            plant.caption_2 = form.cleaned_data.get('caption_2')

            if 'image_3' in request.FILES:
                if (plant.image_3):
                    os.remove(plant.image_3.path)
                plant.image_3 = request.FILES['image_3']
            plant.caption_3 = form.cleaned_data.get('caption_3') 

            if 'image_4' in request.FILES:
                if (plant.image_4):
                    os.remove(plant.image_4.path)
                plant.image_4 = request.FILES['image_4']
            plant.caption_4 = form.cleaned_data.get('caption_4') 

            plant.creator_notes = form.cleaned_data.get('creator_notes') 
            # Build list of bloom months
            plant.bloom_months = bloom_month_list(plant.bloom_start, plant.bloom_end, month_opt)   
            plant.save()

            # Add the selected pests to the selected plant
            pest_list = request.POST.getlist('pest_list')
            pests = Pest.objects.all()
            for pest_item in pest_list:
                for pest in pests:
                    if (pest.pest_name == pest_item):
                        print("DEBUG: pest_name =", pest.pest_name)
                        pest.plants.add(plant)

        return HttpResponseRedirect(reverse('plants:plants_summary'))
    else:
        # convert string-based lists (retrieved from db) to true Python lists
        bloom_color_list  = string2list(plant.bloom_color)
        bloom_season_list = string2list(plant.bloom_season)
        pollinators_list  = string2list(plant.pollinators)
        sun_exposure_list = string2list(plant.sun_exposure)
        soil_type_list    = string2list(plant.soil_type)
        # Get the full list of pests in the database
        pests = Pest.objects.all()
        # Get the pests currently associated with this particular plant
        pests_current = Pest.objects.filter(plants__id=plant.id).order_by('pest_name')
        pest_name_list = []
        pest_tbd_checked = True
        for pest in pests_current:
            pest_name_list.append(pest.pest_name)
        if pest_name_list:
            pest_tbd_checked = False
        print("DEBUG: pest_name_list:", pest_name_list)
        # set the update form with the current db values
        form = PlantAddUpdateForm(initial={ 'commonName'        : plant.commonName,
                                            'type_x'            : plant.type_x,
                                            'bloom_color'       : bloom_color_list,
                                            'bloom_season'      : bloom_season_list,
                                            'bloom_start'       : plant.bloom_start,
                                            'bloom_end'         : plant.bloom_end,
                                            'height_feet'       : plant.height_feet,
                                            'height_inch'       : plant.height_inch,
                                            'width_feet'        : plant.width_feet,
                                            'width_inch'        : plant.width_inch,
                                            'pollinators'       : pollinators_list,
                                            'ca_native'         : plant.ca_native,
                                            'ucd_all_star'      : plant.ucd_all_star,
                                            'sun_exposure'      : sun_exposure_list,
                                            'water_rqmts'       : plant.water_rqmts,
                                            'pH_min'            : plant.pH_min,
                                            'pH_max'            : plant.pH_max,
                                            'soil_type'         : soil_type_list,
                                            'usda_zone_max'     : plant.usda_zone_max,
                                            'usda_zone_min'     : plant.usda_zone_min,
                                            'sunset_zones'      : plant.sunset_zones,
                                            'description'       : plant.description,
                                            'pruning'           : plant.pruning,
                                            'fertilization'     : plant.fertilization,
                                            'propagation  '     : plant.propagation,
                                            'pests_diseases'    : plant.pests_diseases,
                                            'kingdom'           : plant.kingdom,
                                            'subkingdom'        : plant.subkingdom,
                                            'superdivision'     : plant.superdivision, 
                                            'division'          : plant.division, 
                                            'class_x'           : plant.class_x,
                                            'subclass'          : plant.subclass,
                                            'order'             : plant.order,
                                            'family'            : plant.family,
                                            'genus'             : plant.genus,
                                            'species'           : plant.species,
                                            'variety'           : plant.variety,
                                            'phonetic_spelling' : plant.phonetic_spelling,
                                            'audio_name'        : plant.audio_name,
                                            'image_1'           : plant.image_1,
                                            'caption_1'         : plant.caption_1,
                                            'image_2'           : plant.image_2,
                                            'caption_2'         : plant.caption_2,
                                            'image_3'           : plant.image_3,
                                            'caption_3'         : plant.caption_3,
                                            'image_4'           : plant.image_4,
                                            'caption_4'         : plant.caption_4,
                                            'creator_notes'     : plant.creator_notes,
                                        })
        context = { 'plant'            : plant, 
                    'pests'            : pests,
                    'pest_name_list'   : pest_name_list,
                    'pest_tbd_checked' : pest_tbd_checked,
                    'form'             : form,
                    'usda_zones_opt'   : usda_zones_opt,
                    'sunset_zones_opt' : sunset_zones_opt }
        return render(request, 'plants/plants_update.html', context)

def plants_comment(request, id):
    """ Associate a comment to a plant """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    plant = Plant.objects.get(id=id)
    comment = Comment()
    if request.POST:
        form = PlantCommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment.author  = request.user.username            #
            comment.subject = form.cleaned_data.get("subject") #
            comment.comment = form.cleaned_data.get("comment") #
            comment.plant = plant                              # link the comment to the specific plant
            comment.save()
        return HttpResponseRedirect(reverse('plants:plants_details', args=(plant.id,))) 
    else:
        form = PlantCommentForm()
        context = { 'plant' : plant,
                    'form'  : form,
                  }
        return render(request, 'plants/plants_comment.html', context)

def plant2garden(request, id):
    """ Add a plant to a garden """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    plant = Plant.objects.get(id=id)
    gardens = Garden.objects.all()
    for garden in gardens:
        # Only the owner of the garden can add plants to their garden
        if (garden.owner == request.user.username):      # Select the garden based upon current user
            plant.gardens.add(garden)                    # Associate the plant to the selected garden
    return HttpResponseRedirect(reverse('plants:plants_summary'))

def plants_delete(request, id):
    """ Delete selected plant from the Plant database table """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    plant = Plant.objects.get(id=id)
    if request.POST:
        plant.delete()
        return HttpResponseRedirect(reverse('plants:plants_summary')) 
    else:
        context = {'plant': plant}
        return render(request, 'plants/plants_delete_modal.html', context)

def plants_glossary(request):
    """ Render the Glossary Page for Gateway Gardens app """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    return render(request, 'plants/plants_glossary.html')

def plants_reference(request):
    """ Render the Reference Page for Gateway Gardens app """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    return render(request, 'plants/plants_reference.html')

def plants_about(request):
    """ Render the About Page for Gateway Gardens app """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    return render(request, 'plants/plants_about.html')

def pest_summary(request):
    """ Render the page to show all pests for Gateway Gardens app """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    pests = Pest.objects.all()
    template = loader.get_template("plants/pest_summary.html")
    context = { 'pests' : pests }
    return HttpResponse(template.render(context, request))

def pest_add(request):
    """ Render the page to add pests to the database for Gateway Gardens app """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    pest = Pest()
    if request.POST:
        print("DEBUG: Got to pest_add - if")
        form = PestAddUpdateForm(request.POST)
        if form.is_valid():
            pest.pest_name = form.cleaned_data.get('pest_name')
            pest.pest_type = form.cleaned_data.get('pest_type')
            pest.pest_url  = form.cleaned_data.get('pest_url')
            pest.save()
        return HttpResponseRedirect(reverse('plants:pest_summary'))
    else:
        print("DEBUG: Got to pest_add - else")
        form = PestAddUpdateForm()
        context = { 'form' : form }
        return render(request, 'plants/pest_add.html', context)
    
def pest_update(request, id):
    """ Render the page to add pests to the database for Gateway Gardens app """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    pest = Pest.objects.get(id=id)
    if request.POST:
        print("DEBUG: Got to pest_update - if")
        form = PestAddUpdateForm(request.POST)
        if form.is_valid():
            pest.pest_name = form.cleaned_data.get('pest_name')
            pest.pest_type = form.cleaned_data.get('pest_type')
            pest.pest_url  = form.cleaned_data.get('pest_url')
            pest.save()
        return HttpResponseRedirect(reverse('plants:pest_summary'))
    else:
        print("DEBUG: Got to pest_update - else")
        form = PestAddUpdateForm(initial={ 'pest_name' : pest.pest_name,
                                           'pest_type' : pest.pest_type,
                                           'pest_url'  : pest.pest_url,
                                            })
        context = { 'form' : form }
        return render(request, 'plants/pest_update.html', context)
    
def pest_delete(request, id):
    """ Delete selected pest from the Pest database table """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    pest = Pest.objects.get(id=id)
    if request.POST:
        pest.delete()
        return HttpResponseRedirect(reverse('plants:pest_summary')) 
    else:
        context = {'pest': pest}
        return render(request, 'plants/pest_delete_modal.html', context)

def user_signup(request):
    """ Render the User Signup Page for Gateway Gardens app """
    if request.POST:
        form = UserSignupForm(request.POST)
        if form.is_valid():
            signup_username   = form.cleaned_data.get('signup_username')
            signup_password   = form.cleaned_data.get('signup_password')
            signup_password_2 = form.cleaned_data.get('signup_password_2')
            email             = form.cleaned_data.get('email')
            first_name        = form.cleaned_data.get('first_name')
            last_name         = form.cleaned_data.get('last_name')
            signup_input_error = "no"
            # Input Validation: username uniqueness
            if User.objects.filter(username=signup_username).exists():
                signup_input_error = "yes"
                messages.error(request, "username has already been taken")
            # Input Validation: username must be at least 4 characters long
            elif (len(signup_username) < 4):
                signup_input_error = "yes"
                messages.error(request, "username must be at least 4 characters long")
            # Input Validation: passwords do not match
            elif (signup_password != signup_password_2):
                signup_input_error = "yes"
                messages.error(request, "passwords do not match")
            # Input Validation: password must be at least 8 characters long
            elif (len(signup_password) < 8):
                signup_input_error = "yes"
                messages.error(request, "password must be at least 8 characters long")
            # Input Validation: password must contain at least one uppercase letter
            elif not any(char.isupper() for char in signup_password):
                signup_input_error = "yes"
                messages.error(request, "password requires at least one uppercase letter")
            # Input Validation: password must contain at least one lowecaser letter
            elif not any(char.islower() for char in signup_password):
                signup_input_error = "yes"
                messages.error(request, "password requires at least one lowercase letter")
            # Input Validation: password must contain at least one number
            elif not any(char.isdigit() for char in signup_password):
                signup_input_error = "yes"
                messages.error(request, "password requires at least one number")
            # Input Validation: password must contain at least one special character
            elif not any(char in "!@#$%^&*()(_+)" for char in signup_password):
                signup_input_error = "yes"
                messages.error(request, "password requires at least one special character '!@#$%^&*()(_+)'")
            # Input Validation: duplicate e-mail
            elif User.objects.filter(email=email).exists():
                signup_input_error = "yes"
                messages.error(request, "email has already been taken")
            # Input Validation: e-mail format
            else:
                try:
                    emailinfo = validate_email(email, check_deliverability=False)
                    email= emailinfo.normalized
                except:
                    signup_input_error = "yes"
                    messages.error(request, "invalid e-mail address'")
            if (signup_input_error == "yes"):
                # AR: Prepopulate fields - the initialization is not working correctly
                form = UserSignupForm(initial={'signup_username'   : signup_username,
                                               'signup_password'   : signup_password,
                                               'email'      : email,
                                               'first_name' : first_name,
                                               'last_name'  : last_name,
                                       })
                context = { 'form'               : form,
                            'signup_input_error' : signup_input_error }
                return render(request, 'plants/index.html', context)
                # return render(request, 'plants/user_signup_modal.html', context)
            else:
                user = User.objects.create_user(signup_username, email, signup_password)
                user.first_name = first_name
                user.last_name  = last_name
                user.save()
                # Add the user to the "Gardener" group - default
                group = Group.objects.get(name='Gardener')
                group.user_set.add(user)
                # Create a Garden object for the user
                garden = Garden()
                garden.owner = signup_username
                garden.name  = signup_username + "'s Garden"
                garden.save()
                # Authenticate the user
                user = authenticate(request, username=signup_username, password=signup_password)
                # Login the user if they have been authenticated else indicate login failure
                if user is not None:
                    login(request, user)
                    return render(request, 'plants/index.html')
                else:
                    # AR: Indicate on password input form that the username and/or password was invalid
                    return render(request, 'plants/index.html')
        return render(request, 'plants/index.html')
    else:
        form = UserSignupForm()
        context = { 'form' : form }
        return render(request, 'plants/user_signup_modal.html', context)
    
def user_update(request):
    """ Render the User Update Page for Gateway Gardens app """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    user = request.user
    if request.POST:
        form = UserUpdateForm(request.POST)
        if form.is_valid():
            new_username   = form.cleaned_data.get('new_username')
            new_password   = form.cleaned_data.get('new_password')
            new_password_2 = form.cleaned_data.get('new_password_2')
            new_email      = form.cleaned_data.get('new_email')
            new_first_name = form.cleaned_data.get('new_first_name')
            new_last_name  = form.cleaned_data.get('new_last_name')
            update_input_error = "no"
            if (new_username != user.username):
                # Input Validation: username uniqueness
                if User.objects.filter(username=new_username).exists():
                    update_input_error = "yes"
                    messages.error(request, "username has already been taken")
                # Input Validation: username must be at least 4 characters long
                elif (len(new_username) < 4):
                    update_input_error = "yes"
                    messages.error(request, "username must be at least 4 characters long")
            elif ((new_password != "") and (new_password_2 != "")):
                # Input Validation: passwords do not match
                if (new_password != new_password_2):
                    update_input_error = "yes"
                    messages.error(request, "passwords do not match")
                # Input Validation: password must be at least 8 characters long
                elif (len(new_password) < 8):
                    update_input_error = "yes"
                    messages.error(request, "password must be at least 8 characters long")
                # Input Validation: password must contain at least one uppercase letter
                elif not any(char.isupper() for char in new_password):
                    update_input_error = "yes"
                    messages.error(request, "password requires at least one uppercase letter")
                # Input Validation: password must contain at least one lowecaser letter
                elif not any(char.islower() for char in new_password):
                    update_input_error = "yes"
                    messages.error(request, "password requires at least one lowercase letter")
                # Input Validation: password must contain at least one number
                elif not any(char.isdigit() for char in new_password):
                    update_input_error = "yes"
                    messages.error(request, "password requires at least one number")
                # Input Validation: password must contain at least one special character
                elif not any(char in "!@#$%^&*()(_+)" for char in new_password):
                    update_input_error = "yes"
                    messages.error(request, "password requires at least one special character '!@#$%^&*()(_+)'")
            elif (new_email != user.email):
                # Input Validation: duplicate e-mail
                if User.objects.filter(email=new_email).exists():
                    update_input_error = "yes"
                    messages.error(request, "email has already been taken")
                # Input Validation: e-mail format
                else:
                    try:
                        emailinfo = validate_email(new_email, check_deliverability=False)
                        new_email= emailinfo.normalized
                    except:
                        update_input_error = "yes"
                        messages.error(request, "invalid e-mail address")
            if (update_input_error == "yes"):
                # Prepopulate fields - the initialization is not working correctly
                form = UserUpdateForm(initial={'new_username'   : new_username,
                                               'new_password'   : new_password,
                                               'new_email'      : new_email,
                                               'new_first_name' : new_first_name,
                                               'new_last_name'  : new_last_name,
                                       })
                context = { 'form'               : form,
                            'update_input_error' : update_input_error }
                return render(request, 'plants/index.html', context)
            else:
                user.username   = new_username
                # Check to see if a new password has been entered
                if new_password:
                    user.set_password(new_password)
                user.email      = new_email
                user.first_name = new_first_name
                user.last_name  = new_last_name
                user.save()
                # If the password has been updated, xplicitly logout the user so that login modal 
                # will be displayed.  Django's default behavior is to require the user to log back 
                # in after a password change
                if new_password:
                    logout(request)
        return render(request, 'plants/index.html')
    else:
        form = UserUpdateForm(initial={'new_username'   : user.username,
                                       'new_password'   : user.password,
                                       'new_email'      : user.email,
                                       'new_first_name' : user.first_name,
                                       'new_last_name'  : user.last_name,
                                       })
        context = { 'form' : form }
        return render(request, 'plants/user_update_modal.html', context)
    
def user_recovery(request):
    """ Render the User Recovery Page for Gateway Gardens app """
    # AR: Implement Account Recovery view 
    if request.POST:
        form = UserRecoveryForm(request.POST)
        if form.is_valid():
            recovery_username   = form.cleaned_data.get('reovery_username')
            recoovery_password   = form.cleaned_data.get('recovery_password')
            # Login the user if they have been authenticated else indicate login failure
            user = request.user
            if user is not None:
                login(request, user)
                return render(request, 'plants/index.html')
            else:
                return render(request, 'plants/index.html')
    else:
        form = UserRecoveryForm()
        context = { 'form' : form }
        return render(request, 'plants/user_recovery_modal.html', context)

def user_login(request):
    """ Render the User Login Page for Gateway Gardens app """
    if request.POST:
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username   = form.cleaned_data.get('username')
            password   = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            # Login the user if they have been authenticated else indicate login failure
            if user is not None:
                login(request, user)
                return render(request, 'plants/index.html')
            else:
                # AR: Indicate on password input form that the username and/or password was invalid
                return render(request, 'plants/index.html')
    else:
        form = UserLoginForm()
        context = { 'form' : form }
        return render(request, 'plants/user_login_modal.html', context)
    
def user_logout(request):
    """ User Logout function for Gateway Gardens app """
    logout(request)
    return render(request, 'plants/index.html')

def my_column_chooser(request):
    """ Capture the columns that the user wants to display in the plant table """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    
    if request.POST:
        form = MyColumnChooserForm(request.POST)
        if form.is_valid():
            my_column_selection = form.cleaned_data.get('my_column_selection')
            # Associate the column selection to the user's garden
            gardens = Garden.objects.filter(owner = request.user.username)
            for garden in gardens:
                if (garden.owner == request.user.username):
                    garden.my_column_selection = my_column_selection
                    garden.save()
        else:
            return HttpResponseRedirect(reverse('myplants:summary')) 
        return HttpResponseRedirect(reverse('plants:myplants_summary'))
    
    else:
        gardens = Garden.objects.filter(owner = request.user.username)
        # Get the user's previously stored column selection list
        for garden in gardens:
            if (garden.owner == request.user.username):
                my_column_selection = garden.my_column_selection
        # convert string-based list (retrieved from db) to true Python lists
        my_column_selection_list  = string2list(my_column_selection)
        form = MyColumnChooserForm(initial = {'my_column_selection' : my_column_selection_list})
        context = {'form' : form }
        return render(request, 'plants/my_column_chooser_modal.html', context)

def column_chooser(request):
    """ Capture the columns that the user wants to display in the plant table """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    
    if request.POST:
        form = ColumnChooserForm(request.POST)
        if form.is_valid():
            column_selection = form.cleaned_data.get('column_selection')
            # Associate the column selection to the user's garden
            gardens = Garden.objects.filter(owner = request.user.username)
            for garden in gardens:
                if (garden.owner == request.user.username):
                    garden.column_selection = column_selection
                    garden.save()
        else:
            return HttpResponseRedirect(reverse('plants:summary')) 
        return HttpResponseRedirect(reverse('plants:plants_summary'))
    
    else:
        gardens = Garden.objects.filter(owner = request.user.username)
        # Get the user's previously stored column selection list
        for garden in gardens:
            if (garden.owner == request.user.username):
                column_selection = garden.column_selection
        # convert string-based list (retrieved from db) to true Python lists
        column_selection_list  = string2list(column_selection)
        form = ColumnChooserForm(initial = {'column_selection' : column_selection_list})
        context = {'form' : form }
        return render(request, 'plants/column_chooser_modal.html', context)

def string2list(string):
    """ Utility: convert list in string form to a list """
    # print('string: ', string)
    temp = string
    temp = temp.replace("[", "")
    temp = temp.replace("'", "")
    temp = temp.replace("]", "")
    temp = temp.split(", ")
    return(temp)

def string_display(string):
    """ Utility: formal string for display """
    temp = string
    temp = temp.replace("[", "")
    temp = temp.replace("'", "")
    temp = temp.replace("]", "")
    return(temp)

def pH_check(target, lower_limit, upper_limit):
    if (target == "Any"):
        hit = True
    elif ((lower_limit == 'tbd') or (upper_limit == 'tbd')):
        hit = True
    elif ((target >= lower_limit) and (target <= upper_limit)):
        hit = True
    else:
        hit = False
    return(hit)

def usda_zone_check(target, lower_limit, upper_limit):
    if target == "Any":
        hit = True
    elif (target.find("a") == 1 or target.find("b")== 1):
        target_adj = "0" + target
    else:
        target_adj = target

    if lower_limit == "tbd":
        lower_limit_adj = "00a"
    elif (lower_limit.find("a") == 1 or lower_limit.find("b")== 1):
        lower_limit_adj = "0" + lower_limit[0:2]
    else:
        lower_limit_adj = lower_limit[0:3]

    if upper_limit == "tbd":
        upper_limit_adj = "99b"
    elif (upper_limit.find("a") == 1 or upper_limit.find("b")== 1):
        upper_limit_adj = "0" + upper_limit[0:2]
    else:
        upper_limit_adj = upper_limit[0:3]

    if (target == "Any"):
        hit = True
    elif (target_adj >= lower_limit_adj) and (target_adj <= upper_limit_adj):
        hit = True
    else:
        hit = False
    return(hit)

def sunset_zone_check(target, range, options):
    zone_list =[]
    if target == "Any" or range == "tbd":
        hit = True
    else:
        # Convert range into a list of single zones or ranges of zones (form of x-y)
        temp_1 = range.strip()
        temp_2 = temp_1.replace(",", "")
        range_adj = temp_2.split()
        # Convert the list into a list of single zones
        for x in range_adj:
            if "-" in x:
                partition = x.partition("-")
                subrange_start = partition[0]
                subrange_end   = partition[2]
                # Search for the subrange starting zone in the complete list of zones
                # Once the subrange starting zone has been found, search for the subrange end zone
                subrange_start_found = False
                for zone in options:
                    if (subrange_start_found == False) and (subrange_start == zone):
                        zone_list.append(zone)
                        subrange_start_found = True
                    elif (subrange_start_found == True) and (subrange_end != zone):
                        zone_list.append(zone)
                    elif (subrange_start_found == True) and (subrange_end == zone):
                        zone_list.append(zone)
                        break
            else:
                zone_list.append(x)
        # Check to determine is target is contained in the list
        if (target in zone_list):
            hit = True
        else:
            hit = False
    return(hit)

def bloom_month_check(target, start, end, options):
    options_2x = options + options
    if (target == "Any") or (start == "tbd") or (start == "None") or (end == "tbd") or (end == "None"):
        hit = True
    else:
        begin = False
        for option in options_2x:
            if option == start:
                begin = True
                countdown = 12
            if begin == True:
                if target == option:
                    hit = True
                    return(hit)
                else:
                    countdown = countdown - 1
                if option == end or countdown == 0:
                    hit = False
                    return(hit)
    return(hit)

def bloom_month_list(start, end, options):
    options_2x = options + options
    list = []
    if (start == "tbd") or (start == "None") or (end == "tbd") or (end == "None"):
       return(list)
    begin = False
    for option in options_2x:
        if option == start:
            begin = True
        if begin:
            list.append(option)
        if begin and option == end:
            return(list)

def fiddle(request):
    """ Render the Fiddle Page for testing of new functions """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    if request.method == 'POST':
        return render(request, 'plants/fiddle.html')
    else:
        return render(request, 'plants/fiddle.html')

def debug(request):
    """ Render the Debug Page for debugging of new functions """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    return render(request, 'plants/debug.html')