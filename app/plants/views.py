from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect # Added for images
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
#
from django.contrib.auth.models import User                        # User signup
from django.contrib.auth        import authenticate, login, logout # User login/logout

from .models import Garden, MyPlant, Plant, Comment, MyPlantComment 
from .forms  import UserSignupForm, UserLoginForm
from .forms  import GardenAddUpdateForm, MyPlantAddUpdateForm, MyPlantCommentForm
from .forms  import PlantAddUpdateForm, PlantCommentForm

import math
import os

# Define attribute select options
plant_types      = ["tbd", "Annual", "Grass", "Groundcover", "Perennial", "Shrub", "Succulent", "Tree", "Vegetable", "Vine"]
sun_exposure_opt = ["tbd", "Full Sun", "Partial Sun", "Partial Shade", "Full Shade"]
water_rqmts_opt  = ["tbd", "Very Low", "Low", "Medium", "High", "Very High"]
ph_opt           = ["tbd", "5.5", "5.6", "5.7", "5.8", "5.9", 
                    "6.0", "6.1", "6.2", "6.3", "6.4", "6.5", "6.6", "6.7", "6.8", "6.9",
                    "7.0", "7.1", "7.2", "7.3", "7.4", "7.5", "7.6", "7.7", "7.8", "7.9",
                    "8.0"]
bloom_color_opt  = ["tbd", "white", "yellow", "red", "pink", "pale pink", "purple", "green", "blue", "orange"]
bloom_season_opt = ["tbd", "Spring", "Summer", "Fall", "Winter", "None"]
pollinators_opt  = ["tbd", "Bees", "Butterfiles", "Hummingbirds", "None"]
ucd_all_star_opt = ["tbd", "Yes", "No"]
ca_native_opt    = ["tbd", "Yes", "No"]
usda_zones       = ["tbd", "1a", "1b", "2a", "2b", "3a", "3b", "4a", "4b", "5a", "5b", "6a", "6b", "7a", "7b", 
                    "8a", "8b", "9a", "9b", "10a", "10b"]
# sunset_zones     = list(range(1, 25))

def index(request):
    """ Render the landing page for Gateway Gardens app """
    return render(request, 'plants/index.html')

def gardens_summary(request):
    """ Render the individual user's garden summary for Gateway Gardens app """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:user_login'))
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

def gardens_add(request):
    """ Add garden to the database """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:user_login'))
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
        return HttpResponseRedirect(reverse('plants:user_login'))
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
        return HttpResponseRedirect(reverse('plants:user_login'))
    my_plants = MyPlant.objects.filter(owner = request.user.username)
    template = loader.get_template('plants/myplants_summary.html')
    for my_plant in my_plants:
        # format multiselect attributes to remove [, ', and ]
        my_plant.sun_exposure = string_display(my_plant.sun_exposure)
    context = { 'my_plants' : my_plants }
    return HttpResponse(template.render(context, request))

def myplants_add(request, id):
    """ Associate a 'plant' to 'my_plant' """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:user_login'))
    plant = Plant.objects.get(id=id)
    my_plant = MyPlant()
    if request.POST:
        form = MyPlantAddUpdateForm(request.POST)
        if form.is_valid():
            my_plant.owner        = request.user.username                 #
            my_plant.date_planted = form.cleaned_data.get("date_planted") #
            my_plant.location     = form.cleaned_data.get("location")     #
            my_plant.sun_exposure = form.cleaned_data.get("sun_exposure") #
            my_plant.pH           = form.cleaned_data.get("pH")           #
            my_plant.soil_type    = form.cleaned_data.get("soil_type")    #
            my_plant.plant        = plant                                 # link my_plant to the specific plant
            my_plant.save()
        return HttpResponseRedirect(reverse('plants:plants_search')) 
    else:
        form = MyPlantAddUpdateForm()
        context = { 'form' : form }
        return render(request, 'plants/myplants_add.html', context)
    
def myplants_update(request, id):
    """ Update details related a specific My Plant """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:user_login'))
    my_plant = MyPlant.objects.get(id=id)
    if request.POST:
        form = MyPlantAddUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            my_plant.date_planted = form.cleaned_data.get("date_planted") #
            my_plant.location     = form.cleaned_data.get("location")     #
            my_plant.sun_exposure = form.cleaned_data.get("sun_exposure") #
            my_plant.pH           = form.cleaned_data.get("pH")           #
            my_plant.soil_type    = form.cleaned_data.get("soil_type")    #
            my_plant.save()
        return HttpResponseRedirect(reverse('plants:myplants_summary')) 
    else:
        # convert string-based lists (retrieved from db) to true Python lists
        sun_exposure_list = string2list(my_plant.sun_exposure)
        # set the update form with the current db values
        form = MyPlantAddUpdateForm(initial={ 'date_planted' : my_plant.date_planted,
                                              'location'     : my_plant.location,
                                              'sun_exposure' : sun_exposure_list,
                                              'pH'           : my_plant.pH,
                                              'soil_type'    : my_plant.soil_type,
                                            })
        context = { 'form' : form }
        return render(request, 'plants/myplants_update.html', context)

def myplants_remove(request, id):
    """ Remove selected plant from the MyPlants database  """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:user_login'))
    #
    plant = Plant.objects.get(id=id)
    if request.POST:
        my_plants = MyPlant.objects.filter(owner = request.user.username) 
        for my_plant in my_plants:
            if my_plant.plant == plant:
                my_plant.delete()
        return HttpResponseRedirect(reverse('plants:plants_search')) 
    else:
        context = { 'plant' : plant }
        return render(request, 'plants/myplants_remove.html', context)

def myplants_details(request, id):
    """ Show a detailed view of a specific plant """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:user_login'))
    # Uses the id to locate the correct record in the MyPlant table
    my_plant = MyPlant.objects.get(id=id)
    # format multiselect attributes to remove [, ', and ]
    my_plant.sun_exposure = string_display(my_plant.sun_exposure)
    plant   = Plant.objects.get(id=my_plant.plant.id)
    # format multiselect attributes to remove [, ', and ] 
    plant.sun_exposure = string_display(plant.sun_exposure)
    plant.water_rqmts  = string_display(plant.water_rqmts)
    plant.bloom_color  = string_display(plant.bloom_color)
    plant.bloom_season = string_display(plant.bloom_season)
    plant.pollinators  = string_display(plant.pollinators)
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
        return HttpResponseRedirect(reverse('plants:user_login'))
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

def plants_search(request):
    """ Render the Searchable summary list of plants with comments for Gateway Gardens app """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:user_login'))
    if request.method == 'POST':                             # Executed when search is initiated
        template = loader.get_template("plants/plants_search.html")
        # Get the search criteria
        type_x_option        = request.POST["type_x_option"]
        sun_exposure_option  = request.POST["sun_exposure_option"]
        water_rqmts_option   = request.POST["water_rqmts_option"]
        bloom_color_option   = request.POST["bloom_color_option"]
        bloom_season_option  = request.POST["bloom_season_option"]
        pollinators_option   = request.POST["pollinators_option"]
        ucd_all_star_option  = request.POST["ucd_all_star_option"]
        ca_native_option     = request.POST["ca_native_option"]
        garden_option        = request.POST["garden_option"]
        # Save the search criteria - will be used to make the fields "sticky"
        type_x_value         = type_x_option
        sun_exposure_value   = sun_exposure_option
        water_rqmts_value    = water_rqmts_option
        bloom_color_value    = bloom_color_option
        bloom_season_value   = bloom_season_option
        pollinators_value    = pollinators_option
        ucd_all_star_value   = ucd_all_star_option
        ca_native_value      = ca_native_option
        garden_value         = garden_option
        # Plant query -> 'all' or those in the garden owned by the current user
        if garden_option == "Mine":
            plants = Plant.objects.filter(gardens__garden_owner=request.user.username)
        else:
            plants = Plant.objects.all()
        # Run through the search criteria to select the plants to show
        for plant in plants:
            if  ((type_x_option       == plant.type_x)       or (type_x_option       == "Any") or (plant.type_x       == "tbd")) and \
                ((sun_exposure_option in plant.sun_exposure) or (sun_exposure_option == "Any") or (plant.sun_exposure == "tbd")) and \
                ((water_rqmts_option  == plant.water_rqmts)  or (water_rqmts_option  == "Any") or (plant.water_rqmts  == "tbd")) and \
                ((bloom_color_option  in plant.bloom_color)  or (bloom_color_option  == "Any") or (plant.bloom_color  == "tbd")) and \
                ((bloom_season_option in plant.bloom_season) or (bloom_season_option == "Any") or (plant.bloom_season == "tbd")) and \
                ((pollinators_option  in plant.pollinators)  or (pollinators_option  == "Any") or (plant.pollinators  == "tbd")) and \
                ((ucd_all_star_option == plant.ucd_all_star) or (ucd_all_star_option == "Any") or (plant.ucd_all_star == "tbd")) and \
                ((ca_native_option    == plant.ca_native)    or (ca_native_option    == "Any") or (plant.ca_native    == "tbd")):
                # format multiselect attributes to remove [, ', and ]
                plant.sun_exposure = string_display(plant.sun_exposure)
                plant.water_rqmts  = string_display(plant.water_rqmts)
                plant.bloom_color  = string_display(plant.bloom_color)
                plant.bloom_season = string_display(plant.bloom_season)
                plant.pollinators  = string_display(plant.pollinators)
                # show selected plant
                plant.plant_show = "yes"
            else:
                plant.plant_show = "no"
        context = { "plants"             : plants,
                    # Search attributes
                    'plant_types'        : plant_types,
                    "sun_exposure_opt"   : sun_exposure_opt,
                    "water_rqmts_opt"    : water_rqmts_opt,
                    "bloom_color_opt"    : bloom_color_opt,
                    "bloom_season_opt"   : bloom_season_opt,
                    "pollinators_opt"    : pollinators_opt,
                    "ucd_all_star_opt"   : ucd_all_star_opt,
                    "ca_native_opt"      : ca_native_opt,
                    # Search option values from previous search if applicable else default of "Any"
                    "type_x_value"       : type_x_value,
                    "sun_exposure_value" : sun_exposure_value,
                    "water_rqmts_value"  : water_rqmts_value,
                    "bloom_color_value"  : bloom_color_value,
                    "bloom_season_value" : bloom_season_value,
                    'pollinators_value'  : pollinators_value,
                    'ucd_all_star_value' : ucd_all_star_value,
                    'ca_native_value'    : ca_native_value,
                    'garden_value'       : garden_value,
                  }
        return render(request, "plants/plants_search.html", context)
    else:                                                       # Executed when search page is initialized
        plants   = Plant.objects.all()
        my_plants = MyPlant.objects.filter(owner = request.user.username)
        # set search field defaults
        type_x_value       = "Any"
        sun_exposure_value = "Any"
        water_rqmts_value  = "Any"
        bloom_color_value  = "Any"
        bloom_season_value = "Any"
        pollinators_value  = "Any"
        ucd_all_star_value = "Any"
        ca_native_value    = "Any"
        garden_value       = "Any"

        for plant in plants:
            # format multiselect attributes to remove [, ', and ]
            plant.sun_exposure = string_display(plant.sun_exposure)
            plant.water_rqmts  = string_display(plant.water_rqmts)
            plant.bloom_color  = string_display(plant.bloom_color)
            plant.bloom_season = string_display(plant.bloom_season)
            plant.pollinators  = string_display(plant.pollinators)
            # show all plants on initial rendering
            plant.plant_show = "yes"
            # check to determine if the current user has already claimed the plant
            plant.plant_mine = "no"
            for my_plant in my_plants:
                if my_plant.plant == plant:
                    plant.plant_mine = "yes"
        template = loader.get_template("plants/plants_search.html")
        context = { "plants"             : plants,
                    "my_plants"          : my_plants,
                    # search field options
                    "plant_types"        : plant_types,
                    "sun_exposure_opt"   : sun_exposure_opt,
                    "water_rqmts_opt"    : water_rqmts_opt,
                    "bloom_color_opt"    : bloom_color_opt,
                    "bloom_season_opt"   : bloom_season_opt,
                    "pollinators_opt"    : pollinators_opt,
                    "ucd_all_star_opt"   : ucd_all_star_opt,
                    "ca_native_opt"      : ca_native_opt,
                    # search field defaults
                    "type_x_value"       : type_x_value,
                    "sun_exposure_value" : sun_exposure_value,
                    "water_rqmts_value"  : water_rqmts_value,
                    "pollinators_value"  : pollinators_value,
                    'ucd_all_star_value' : ucd_all_star_value,
                    'ca_native_value'    : ca_native_value,
                    'garden_value'       : garden_value,
              }
    return HttpResponse(template.render(context, request))

def plants_details(request, id):
    """ Show a detailed view of a specific plant """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:user_login'))
    plant = Plant.objects.get(id=id)                     # Uses the id to locate the correct record in the Plant table
    comments = Comment.objects.filter(plant__pk=id)      # get all comments related to the plant
    # format multiselect attributes to remove [, ', and ]
    plant.sun_exposure = string_display(plant.sun_exposure)
    plant.water_rqmts  = string_display(plant.water_rqmts)
    plant.bloom_color  = string_display(plant.bloom_color)
    plant.bloom_season = string_display(plant.bloom_season)
    plant.pollinators  = string_display(plant.pollinators)

    if (plant.height_inch != 0):
        height_adj = plant.height_feet + (plant.height_inch / 12)
        plant.height_feet = math.floor(height_adj)
        plant.height_inch = plant.height_inch%12
    if (plant.width_inch != 0):
        width_adj = plant.width_feet + (plant.width_inch / 12)
        plant.width_feet = math.floor(width_adj)
        plant.width_inch = plant.width_inch%12
    template = loader.get_template("plants/plants_details.html")  # loads the plant_details.html template
    context = { "plant"    : plant, 
                "comments" : comments, 
            }
    return HttpResponse(template.render(context, request)) # Send "context" to template and output the html from the template

def plants_add(request):
    """ Render the page to add plants to the database for Gateway Gardens app """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:user_login'))
    plant = Plant()
    if request.POST:
        form = PlantAddUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            plant.commonName    = form.cleaned_data.get('commonName')
            plant.type_x        = form.cleaned_data.get('type_x')
            plant.bloom_color   = form.cleaned_data.get('bloom_color')
            plant.bloom_season  = form.cleaned_data.get('bloom_season')
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
            plant.pronunciation = form.cleaned_data.get('pronunciation')
            plant.description   = form.cleaned_data.get('description')
            plant.pruning       = form.cleaned_data.get('pruning')
            plant.fertilization = form.cleaned_data.get('fertilization')
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
            plant.save()
        return HttpResponseRedirect(reverse('plants:plants_search'))
    else:
        form = PlantAddUpdateForm()
        context = { 'form' : form }
        return render(request, 'plants/plants_add.html', context)

def plants_update(request, id):
    """ Update the attributes for an existing plant """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:user_login'))
    plant = Plant.objects.get(id=id)
    if request.POST:
        form = PlantAddUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            plant.commonName    = form.cleaned_data.get('commonName')
            plant.type_x        = form.cleaned_data.get('type_x')
            plant.bloom_color   = form.cleaned_data.get('bloom_color')
            plant.bloom_season  = form.cleaned_data.get('bloom_season')
            plant.height_feet   = form.cleaned_data.get('height_feet')
            plant.height_inch   = form.cleaned_data.get('height_inch')
            plant.width_feet    = form.cleaned_data.get('width_feet')
            plant.width_inch    = form.cleaned_data.get('width_inch')
            plant.sun_exposure  = form.cleaned_data.get('sun_exposure')
            plant.water_rqmts   = form.cleaned_data.get('water_rqmts')
            plant.pH_min        = form.cleaned_data.get('pH_min')
            plant.pH_max        = form.cleaned_data.get('pH_max')
            plant.soil_type     = form.cleaned_data.get('soil_type')
            plant.pollinators   = form.cleaned_data.get('pollinators')
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
            plant.pronunciation = form.cleaned_data.get('pronunciation')
            plant.description   = form.cleaned_data.get('description')
            plant.pruning       = form.cleaned_data.get('pruning')
            plant.fertilization = form.cleaned_data.get('fertilization')
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
            plant.save()
        return HttpResponseRedirect(reverse('plants:plants_search'))
    else:
        # convert string-based lists (retrieved from db) to true Python lists
        bloom_color_list  = string2list(plant.bloom_color)
        bloom_season_list = string2list(plant.bloom_season)
        pollinators_list  = string2list(plant.pollinators)
        sun_exposure_list = string2list(plant.sun_exposure)
        soil_type_list    = string2list(plant.soil_type)
        # set the update form with the current db values
        form = PlantAddUpdateForm(initial={ 'commonName'    : plant.commonName,
                                            'type_x'        : plant.type_x,
                                            'bloom_color'   : bloom_color_list,
                                            'bloom_season'  : bloom_season_list,
                                            'height_feet'   : plant.height_feet,
                                            'height_inch'   : plant.height_inch,
                                            'width_feet'    : plant.width_feet,
                                            'width_inch'    : plant.width_inch,
                                            'pollinators'   : pollinators_list,
                                            'sun_exposure'  : sun_exposure_list,
                                            'water_rqmts'   : plant.water_rqmts,
                                            'pH_min'        : plant.pH_min,
                                            'pH_max'        : plant.pH_max,
                                            'soil_type'     : soil_type_list,
                                            'ucd_all_star'  : plant.ucd_all_star,
                                            'ca_native'     : plant.ca_native,
                                            'usda_zone_max' : plant.usda_zone_max,
                                            'usda_zone_min' : plant.usda_zone_min,
                                            'sunset_zones'  : plant.sunset_zones,
                                            'description'   : plant.description,
                                            'pruning'       : plant.pruning,
                                            'fertilization' : plant.fertilization,
                                            'kingdom'       : plant.kingdom,
                                            'subkingdom'    : plant.subkingdom,
                                            'superdivision' : plant.superdivision, 
                                            'division'      : plant.division, 
                                            'class_x'       : plant.class_x,
                                            'subclass'      : plant.subclass,
                                            'order'         : plant.order,
                                            'family'        : plant.family,
                                            'genus'         : plant.genus,
                                            'species'       : plant.species,
                                            'variety'       : plant.variety,
                                            'pronunciation' : plant.pronunciation,
                                            'image_1'       : plant.image_1,
                                            'image_2'       : plant.image_2,
                                            'image_3'       : plant.image_3,
                                            'image_4'       : plant.image_4,
                                            'creator_notes' : plant.creator_notes,
                                        })
        context = { 'plant' : plant, 'form' : form }
        return render(request, 'plants/plants_update.html', context)

def plants_comment(request, id):
    """ Associate a comment to a plant """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:user_login'))
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
        return HttpResponseRedirect(reverse('plants:user_login'))
    plant = Plant.objects.get(id=id)
    gardens = Garden.objects.all()
    for garden in gardens:
        # Only the owner of the garden can add plants to their garden
        if (garden.owner == request.user.username):      # Select the garden based upon current user
            plant.gardens.add(garden)                    # Associate the plant to the selected garden
    return HttpResponseRedirect(reverse('plants:plants_search'))

def plants_delete(request, id):
    """ Delete selected plant from the database  """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:user_login'))
    plant = Plant.objects.get(id=id)
    if request.POST:
      plant.delete()
      return HttpResponseRedirect(reverse('plants:plants_search')) 
    context = {'plant': plant}
    return render(request, 'plants/plants_delete.html', context)

def plants_glossary(request):
    """ Render the Glossary Page for Gateway Gardens app """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:user_login'))
    return render(request, 'plants/plants_glossary.html')

def plants_reference(request):
    """ Render the Reference Page for Gateway Gardens app """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:user_login'))
    return render(request, 'plants/plants_reference.html')

def plants_about(request):
    """ Render the About Page for Gateway Gardens app """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:user_login'))
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
        username   = request.POST.get('username')
        password   = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        # Login the user if they have been authenticated else indicate login failure
        if user is not None:
            login(request, user)
            return render(request, 'plants/index.html')
        else:
            # AR: Indicate on password input form that the username and/or password was invalid
            return render(request, 'plants/index.html')
    else:
        return render(request, 'plants/user_login_modal.html')
    
def user_logout(request):
    """ User Logout function for Gateway Gardens app """
    logout(request)
    return render(request, 'plants/index.html')

def string2list(string):
    """ Utility: convert list in string form to a list """
    # print('string: ', string)
    temp = string
    temp = temp.replace("[", "")
    temp = temp.replace("'", "")
    temp = temp.replace("]", "")
    temp = temp.split(", ")
    # print('list: ', temp)
    return(temp)

def string_display(string):
    """ Utility: formal string for display """
    temp = string
    temp = temp.replace("[", "")
    temp = temp.replace("'", "")
    temp = temp.replace("]", "")
    return(temp)