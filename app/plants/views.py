# /app/plants/views.py

import math
 
from django.http      import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.shortcuts import render, redirect # Added for images
from django.template  import loader
from django.urls      import reverse
from django.db.models import Q # used to create complex database queries that involve logical operators such as OR, AND, and NOT

from mygarden.models  import Garden
from myplants.models  import MyPlant
from .models          import Plant, Comment
from pests.models     import Pest

from .forms           import PlantAddUpdateForm, PlantCommentForm, ColumnChooserForm

from core_utils.helpers import string2list, string_display
from core_utils.helpers import pH_check, usda_zone_check, sunset_zone_check, bloom_month_check, bloom_month_list

# Define attribute select option arrays
plant_types      = ["tbd", "Annual", "Bulb", "Fern", "Grass", "Turf Grass", 
                    "Groundcover", "Perennial", "Shrub", "Forb", "Succulent", 
                    "Tree-Deciduous", "Tree-Evergreen", "Vegetable", "Vine"]
bloom_color_opt  = ["tbd", "white", "creamy white", "yellow", "red", "burgundy", "pink", "pale pink", 
                    "lavendar", "purple", "green", "blue", "orange", "none"]
bloom_season_opt = ["tbd", "Spring", "Summer", "Fall", "Winter", "Infrequent", "None"]
pollinators_opt  = ["tbd", "Bees", "Butterflies", "Hummingbirds", "None"]
ca_native_opt    = ["tbd", "Yes", "No"]
ucd_all_star_opt = ["Yes", "No"]
davis_trees_opt  = ["Yes", "No"]
sunset_z14_opt   = ["tbd", "Yes", "No"]
sun_exposure_opt = ["tbd", "Full Sun", "Partial Sun", "Partial Shade", "Full Shade", "Afternoon Shade"]
water_rqmts_opt  = ["tbd", "Very Low", "Low", "Medium", "High", "Very High"]
pH_opt           = ["tbd", 
                    "5.0", "5.1", "5.2", "5.3", "5.4", "5.5", "5.6", "5.7", "5.8", "5.9", 
                    "6.0", "6.1", "6.2", "6.3", "6.4", "6.5", "6.6", "6.7", "6.8", "6.9",
                    "7.0", "7.1", "7.2", "7.3", "7.4", "7.5", "7.6", "7.7", "7.8", "7.9",
                    "8.0"]
soil_type_opt       = ["tbd", "Sandy", "Loamy", "Clay"]
heat_tolerance_opt  = ["tbd", "Poor", "Fair", "Good", "Excellent"]
deer_resistance_opt = ["tbd", "Poor", "Fair", "Good", "Excellent"]
usda_zones_opt     = ["tbd", "1a", "1b",  "2a",  "2b",  "3a",  "3b", "4a", "4b",
                             "5a", "5b",  "6a",  "6b",  "7a",  "7b", "8a", "8b",
                             "9a", "9b", "10a", "10b", "11a", "11b"]
sunset_zones_opt = ["1A", "1B", "2A", "2B", "3A", "3B",  "4",  "5",  "6",  "7",  "8",  "9", "10", 
                    "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", 
                    "21", "22", "23", "24", "28", "29", "30", "31", "32", "33", "34", "35",
                    "A1", "A2", "A3", "H1", "H2"]
happiness_opt    = ["tbd", "Very Happy", "Happy", "Neutral", "Unhappy", "Very Unhappy"]
month_opt        = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

todo_action_opt  = ["Fertilize", "Harvest", "Mow", "Plant", "Prune", "Spray", "Other"]
todo_repeat_opt  = ["Daily", "Weekly", "Bi-Weekly", "Monthly", "Yearly", "Never"]
status_opt       = ["Development", "Review", "Published", "Archived"]

def plants_summary(request):
    """ Render the Searchable summary list of plants with comments for Gateway Gardens app """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    
    # Obtain the user's saved configuration information
    user_info = request.user.userinfo

    #-----------------------------------------------------------------------------------------------------
    # Executed when search request is submitted
    #-----------------------------------------------------------------------------------------------------
    if request.method == 'POST':   
        # Get the search criteria from the "http request"
        common_name_search     = request.POST["common_name_search"]
        genus_search           = request.POST["genus_search"]
        species_search         = request.POST["species_search"]
        type_x_search          = request.POST["type_x_search"]
        bloom_color_search     = request.POST["bloom_color_search"]
        bloom_season_search    = request.POST["bloom_season_search"]
        bloom_month_search     = request.POST["bloom_month_search"]
        pollinators_search     = request.POST["pollinators_search"]
        ca_native_search       = request.POST["ca_native_search"]
        ucd_all_star_search    = request.POST["ucd_all_star_search"]
        davis_trees_search     = request.POST["davis_trees_search"]
        sunset_z14_search      = request.POST["sunset_z14_search"]
        sun_exposure_search    = request.POST["sun_exposure_search"]
        water_rqmts_search     = request.POST["water_rqmts_search"]
        pH_search              = request.POST["pH_search"]
        soil_type_search       = request.POST["soil_type_search"]
        heat_tolerance_search  = request.POST["heat_tolerance_search"]
        deer_resistance_search = request.POST["deer_resistance_search"]
        usda_zone_search       = request.POST["usda_zone_search"]
        sunset_zone_search     = request.POST["sunset_zone_search"]
        garden_search          = request.POST["garden_search"]
        status_search          = request.POST["status_search"]

        # Save the search criteria
        user_info.common_name_search     = common_name_search
        user_info.genus_search           = genus_search
        user_info.species_search         = species_search
        user_info.type_x_search          = type_x_search
        user_info.bloom_color_search     = bloom_color_search
        user_info.bloom_season_search    = bloom_season_search
        user_info.bloom_month_search     = bloom_month_search
        user_info.pollinators_search     = pollinators_search
        user_info.ca_native_search       = ca_native_search
        user_info.ucd_all_star_search    = ucd_all_star_search
        user_info.davis_trees_search     = davis_trees_search
        user_info.sunset_z14_search      = sunset_z14_search
        user_info.sun_exposure_search    = sun_exposure_search
        user_info.water_rqmts_search     = water_rqmts_search
        user_info.pH_search              = pH_search
        user_info.soil_type_search       = soil_type_search
        user_info.heat_tolerance_search  = heat_tolerance_search
        user_info.deer_resistance_search = deer_resistance_search
        user_info.usda_zone_search       = usda_zone_search
        user_info.sunset_zone_search     = sunset_zone_search
        user_info.garden_search          = garden_search
        user_info.status_search          = status_search
        user_info.save()
    #-----------------------------------------------------------------------------------------------------
    # Executed when plants summary page is initialized
    #-----------------------------------------------------------------------------------------------------
    else:
        # Get the user's previously stored search criteria
        common_name_search     = user_info.common_name_search
        genus_search           = user_info.genus_search
        species_search         = user_info.species_search
        type_x_search          = user_info.type_x_search
        bloom_color_search     = user_info.bloom_color_search
        bloom_season_search    = user_info.bloom_season_search
        bloom_month_search     = user_info.bloom_month_search
        pollinators_search     = user_info.pollinators_search
        ca_native_search       = user_info.ca_native_search
        ucd_all_star_search    = user_info.ucd_all_star_search
        davis_trees_search     = user_info.davis_trees_search
        sunset_z14_search      = user_info.sunset_z14_search
        sun_exposure_search    = user_info.sun_exposure_search
        water_rqmts_search     = user_info.water_rqmts_search
        pH_search              = user_info.pH_search
        soil_type_search       = user_info.soil_type_search
        heat_tolerance_search  = user_info.heat_tolerance_search
        deer_resistance_search = user_info.deer_resistance_search
        usda_zone_search       = user_info.usda_zone_search
        sunset_zone_search     = user_info.sunset_zone_search
        garden_search          = user_info.garden_search
    #-----------------------------------------------------------------------------------------------------
    # Execute the search
    #-----------------------------------------------------------------------------------------------------
    # Get the user's previously stored column display sections
    column_selection_list  = string2list(user_info.column_selection)

    # If user not a "Garden-Editor" set to "Published"
    if request.user.groups.filter(name='Garden-Editor').exists(): 
        status_search = user_info.status_search
    else:
        status_search = "Published"

    # Obtain the plants that the current user has claimed for their garden
    myplants = MyPlant.objects.filter(owner = request.user.username) 
    
    # Filter the plants db - "My plants" and "Common Name" substring
    if garden_search == "In My Garden":
        plants = Plant.objects.filter(
            Q(myplants__owner       = request.user.username) & 
            Q(myplants__status      = "in_my_garden")        &
            Q(commonName__icontains = common_name_search)    &
            Q(genus__icontains      = genus_search)          &
            Q(species__icontains    = species_search)
        ).order_by("commonName")
    elif garden_search == "My Wish List":
        plants = Plant.objects.filter(
            Q(myplants__owner       = request.user.username) & 
            Q(myplants__status      = "wish_list")           & 
            Q(commonName__icontains = common_name_search)    &
            Q(genus__icontains      = genus_search)          &
            Q(species__icontains    = species_search)
        ).order_by("commonName")
    else:
        plants = Plant.objects.filter(
            Q(commonName__icontains = common_name_search)    &
            Q(genus__icontains      = genus_search)          &
            Q(species__icontains    = species_search)
        ).order_by("commonName")

    # Run through the search criteria to select the plants to show
    for plant in plants:
        pH_hit = pH_check(pH_search, plant.pH_min, plant.pH_max)
        usda_zone_hit = usda_zone_check(usda_zone_search, plant.usda_zone_min, plant.usda_zone_max)
        sunset_zone_hit = sunset_zone_check(sunset_zone_search, plant.sunset_zones, sunset_zones_opt)
        bloom_month_hit = bloom_month_check(bloom_month_search, plant.bloom_start, plant.bloom_end, month_opt)
        if  ((type_x_search          == plant.type_x)          or (type_x_search          == "Any")) and \
            ((bloom_color_search     in plant.bloom_color)     or (bloom_color_search     == "Any")) and \
            ((bloom_season_search    in plant.bloom_season)    or (bloom_season_search    == "Any")) and \
            ((pollinators_search     in plant.pollinators)     or (pollinators_search     == "Any")) and \
            ((ca_native_search       == plant.ca_native)       or (ca_native_search       == "Any")) and \
            ((ucd_all_star_search    == plant.ucd_all_star)    or (ucd_all_star_search    == "Any")) and \
            ((davis_trees_search     == plant.davis_trees)     or (davis_trees_search     == "Any")) and \
            ((sunset_z14_search      == plant.sunset_z14)      or (sunset_z14_search      == "Any")) and \
            ((sun_exposure_search    in plant.sun_exposure)    or (sun_exposure_search    == "Any")) and \
            ((water_rqmts_search     == plant.water_rqmts)     or (water_rqmts_search     == "Any")) and \
            ((soil_type_search       in plant.soil_type)       or (soil_type_search       == "Any")) and \
            ((heat_tolerance_search  == plant.heat_tolerance)  or (heat_tolerance_search  == "Any")) and \
            ((deer_resistance_search == plant.deer_resistance) or (deer_resistance_search == "Any")) and \
            ((status_search          == plant.status)          or (status_search          == "Any")) and \
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
        plant.bloom_color     = string_display(plant.bloom_color)
        plant.bloom_season    = string_display(plant.bloom_season)
        plant.bloom_months    = string_display(plant.bloom_months)
        plant.pollinators     = string_display(plant.pollinators)
        plant.sun_exposure    = string_display(plant.sun_exposure)
        plant.water_rqmts     = string_display(plant.water_rqmts)
        plant.soil_type       = string_display(plant.soil_type)
        plant.heat_tolerance  = string_display(plant.heat_tolerance)
        plant.deer_resistance = string_display(plant.deer_resistance)

        # Create short version of usda_zones for table display
        plant.usda_zone_min = plant.usda_zone_min.split()[0]
        plant.usda_zone_max = plant.usda_zone_max.split()[0]

        # Set the plant status regarding its status wrt my_plants 
        plant.plant_mine = 'not_in_my_garden'
        for myplant in myplants:
            if myplant.plant == plant:
                if myplant.status == 'in_my_garden':
                    plant.plant_mine = 'in_my_garden' 
                    break # Found the plant in myplants  
                elif myplant.status == 'wish_list':
                    plant.plant_mine = 'wish_list'
                    break # Found the plant in myplants

    # Send selected plant details to template
    context = { "plants"                 : plants,
                "myplants"               : myplants,
                # search field options
                "plant_types"            : plant_types,
                "bloom_color_opt"        : bloom_color_opt,
                "bloom_season_opt"       : bloom_season_opt,
                "pollinators_opt"        : pollinators_opt,
                "ca_native_opt"          : ca_native_opt,
                "ucd_all_star_opt"       : ucd_all_star_opt,
                "davis_trees_opt"        : davis_trees_opt,
                "sunset_z14_opt"         : sunset_z14_opt,
                "sun_exposure_opt"       : sun_exposure_opt,
                "water_rqmts_opt"        : water_rqmts_opt,
                "pH_opt"                 : pH_opt,
                "soil_type_opt"          : soil_type_opt,
                "heat_tolerance_opt"     : heat_tolerance_opt,
                "deer_resistance_opt"    : deer_resistance_opt,
                "usda_zones_opt"         : usda_zones_opt,
                "sunset_zones_opt"       : sunset_zones_opt,
                "month_opt"              : month_opt,
                # Admin
                "status_opt"             : status_opt,
                # search field defaults
                "common_name_search"     : common_name_search,
                "genus_search"           : genus_search,
                "species_search"         : species_search,
                "type_x_search"          : type_x_search,
                "bloom_color_search"     : bloom_color_search,
                "bloom_season_search"    : bloom_season_search,
                "bloom_month_search"     : bloom_month_search,
                "pollinators_search"     : pollinators_search,
                'ca_native_search'       : ca_native_search,
                'ucd_all_star_search'    : ucd_all_star_search,
                'davis_trees_search'     : davis_trees_search,
                'sunset_z14_search'      : sunset_z14_search,
                "sun_exposure_search"    : sun_exposure_search,
                "water_rqmts_search"     : water_rqmts_search,
                "soil_type_search"       : soil_type_search,
                "pH_search"              : pH_search,
                "heat_tolerance_search"  : heat_tolerance_search,
                "deer_resistance_search" : deer_resistance_search,
                "usda_zone_search"       : usda_zone_search,
                "sunset_zone_search"     : sunset_zone_search,
                'garden_search'          : garden_search,
                # Admin
                'status_search'          : status_search,
                # table column selection
                'column_selection'       : column_selection_list,
              }
    template = loader.get_template("plants/plants_summary.html")
    return HttpResponse(template.render(context, request))

def plant_details(request, id):
    """ Show a detailed view of a specific plant """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    plant = Plant.objects.get(id=id)             
    # get all comments related to the selected plant        
    comments = Comment.objects.filter(plant__pk=id)      
    # format multiselect attributes to remove [, ', and ]
    plant.sun_exposure = string_display(plant.sun_exposure)
    plant.water_rqmts  = string_display(plant.water_rqmts)
    plant.bloom_color  = string_display(plant.bloom_color)
    plant.bloom_season = string_display(plant.bloom_season)
    plant.pollinators  = string_display(plant.pollinators)
    plant.soil_type    = string_display(plant.soil_type)
    plant.heat_tolerance = string_display(plant.heat_tolerance)

    if (plant.height_inch != 0):
        height_adj = plant.height_feet + (plant.height_inch / 12)
        plant.height_feet = math.floor(height_adj)
        plant.height_inch = plant.height_inch%12
    if (plant.width_inch != 0):
        width_adj = plant.width_feet + (plant.width_inch / 12)
        plant.width_feet = math.floor(width_adj)
        plant.width_inch = plant.width_inch%12
    template = loader.get_template("plants/plant_details.html")  # loads the plant_details.html template
    # Get the pests associated with this plant & sort by pest name
    pests = Pest.objects.filter(plants__id=plant.id).order_by('pest_name')
    form = PlantCommentForm()
    context = { "plant"    : plant, 
                "pests"    : pests,    
                "comments" : comments, 
                "form"     : form,
            }
    return HttpResponse(template.render(context, request))

def plant_add(request):
    """ Render the page to add plants to the database for Gateway Gardens app """
    if not request.user.groups.filter(name='Garden-Editor').exists():
        return HttpResponseRedirect(reverse('general:index'))
    # Create a new plant and save it to obtain an ID
    plant = Plant()
    plant.save()
    # Give the new plant a default common name and status
    plant.commonName = "< New Plant " + str(plant.id) + " >"
    plant.status     = "Development"
    plant.creator    = request.user.username
    plant.save()
    # Edit the newly created plant
    return HttpResponseRedirect(reverse('plants:plant_edit', args=(plant.id,))) 

def plant_edit(request, id):
    """ Update the attributes for an existing plant """
    if not request.user.groups.filter(name='Garden-Editor').exists():
        return HttpResponseRedirect(reverse('general:index'))
    plant = Plant.objects.get(id=id)
    if request.method == "POST":
        form = PlantAddUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            plant.status          = form.cleaned_data.get('status')
            plant.commonName      = form.cleaned_data.get('commonName')
            plant.type_x          = form.cleaned_data.get('type_x')
            plant.bloom_color     = form.cleaned_data.get('bloom_color')
            plant.bloom_season    = form.cleaned_data.get('bloom_season')
            plant.bloom_start     = form.cleaned_data.get('bloom_start')
            plant.bloom_end       = form.cleaned_data.get('bloom_end')
            plant.height_feet     = form.cleaned_data.get('height_feet')
            plant.height_inch     = form.cleaned_data.get('height_inch')
            plant.width_feet      = form.cleaned_data.get('width_feet')
            plant.width_inch      = form.cleaned_data.get('width_inch')
            plant.pollinators     = form.cleaned_data.get('pollinators')
            plant.ca_native       = form.cleaned_data.get('ca_native')
            plant.ucd_all_star    = form.cleaned_data.get('ucd_all_star')
            plant.davis_trees     = form.cleaned_data.get('davis_trees')
            plant.sunset_z14      = form.cleaned_data.get('sunset_z14')
            plant.sun_exposure    = form.cleaned_data.get('sun_exposure')
            plant.water_rqmts     = form.cleaned_data.get('water_rqmts')
            plant.pH_min          = form.cleaned_data.get('pH_min')
            plant.pH_max          = form.cleaned_data.get('pH_max')
            plant.soil_type       = form.cleaned_data.get('soil_type')
            plant.heat_tolerance  = form.cleaned_data.get('heat_tolerance')
            plant.deer_resistance = form.cleaned_data.get('deer_resistance')
            plant.usda_zone_min   = form.cleaned_data.get('usda_zone_min')
            plant.usda_zone_max   = form.cleaned_data.get('usda_zone_max')
            plant.sunset_zones    = form.cleaned_data.get('sunset_zones')
            plant.kingdom         = form.cleaned_data.get('kingdom')
            plant.subkingdom      = form.cleaned_data.get('subkingdom')
            plant.superdivision   = form.cleaned_data.get('superdivision')
            plant.division        = form.cleaned_data.get('division')
            plant.class_x         = form.cleaned_data.get('class_x')
            plant.subclass        = form.cleaned_data.get('subclass')
            plant.order           = form.cleaned_data.get('order')
            plant.family          = form.cleaned_data.get('family')
            plant.genus           = form.cleaned_data.get('genus')
            plant.species         = form.cleaned_data.get('species')
            plant.subspecies      = form.cleaned_data.get('subspecies')
            plant.variety         = form.cleaned_data.get('variety')
            plant.cultivar        = form.cleaned_data.get('cultivar')
            plant.phonetic_spelling = form.cleaned_data.get('phonetic_spelling')

            # Check to see if the request includes an audio file for genus/species
            if 'audioBlob' in request.FILES:
                # Check to if there is an exiting audio file for the plant in the db
                if (plant.audio_name):
                    plant.audio_name.delete(save=False)
                plant.audio_name = request.FILES['audioBlob']
                
            plant.description    = form.cleaned_data.get('description')
            plant.pruning        = form.cleaned_data.get('pruning')
            plant.pruning_video  = form.cleaned_data.get('pruning_video')
            plant.fertilization  = form.cleaned_data.get('fertilization')
            plant.propagation    = form.cleaned_data.get('propagation')
            plant.pests_diseases = form.cleaned_data.get('pests_diseases')

            # Process images - check for new image - if yes, delete any existing image
            if 'image_1' in request.FILES:
                if (plant.image_1):
                    plant.image_1.delete(save=False)
                plant.image_1 = request.FILES['image_1']
            plant.caption_1 = form.cleaned_data.get('caption_1')
            
            if 'image_2' in request.FILES:
                if (plant.image_2):
                    plant.image_2.delete(save=False)
                plant.image_2 = request.FILES['image_2']
            plant.caption_2 = form.cleaned_data.get('caption_2')

            if 'image_3' in request.FILES:
                if (plant.image_3):
                    plant.image_3.delete(save=False)
                plant.image_3 = request.FILES['image_3']
            plant.caption_3 = form.cleaned_data.get('caption_3') 

            if 'image_4' in request.FILES:
                if (plant.image_4):
                    plant.image_4.delete(save=False)
                plant.image_4 = request.FILES['image_4']
            plant.caption_4 = form.cleaned_data.get('caption_4') 
            # Admin
            plant.creator_notes = form.cleaned_data.get('creator_notes') 
            plant.status = form.cleaned_data.get('status')
            # Build list of bloom months
            plant.bloom_months = bloom_month_list(plant.bloom_start, plant.bloom_end, month_opt)   
            plant.save()

            # Add the selected pests to the selected plant
            pest_list = request.POST.getlist('pest_list')
            pests = Pest.objects.all().order_by('pest_type', 'pest_name')
            for pest_item in pest_list:
                for pest in pests:
                    if (pest.pest_name == pest_item):
                        pest.plants.add(plant)
        response_data = {
            'status': 'success',
            'message': f'Received audio successfully',
            # 'file_size': audio_file.size
        }
        return JsonResponse(response_data)
    else:
        # convert string-based lists (retrieved from db) to true Python lists
        bloom_color_list  = string2list(plant.bloom_color)
        bloom_season_list = string2list(plant.bloom_season)
        pollinators_list  = string2list(plant.pollinators)
        sun_exposure_list = string2list(plant.sun_exposure)
        soil_type_list    = string2list(plant.soil_type)
        # Get the full list of pests in the database

        pests = Pest.objects.filter( Q(pest_type = 'Insect' ) | Q(pest_type = 'Disease') | Q(pest_type = 'Mollusk') ).order_by('pest_type', 'pest_name')
        # pests = Pest.objects.all().order_by('pest_type', 'pest_name')
        
        # Get the pests currently associated with this particular plant
        pests_current = Pest.objects.filter(plants__id=plant.id).order_by('pest_type', 'pest_name')
        pest_name_list = []
        pest_tbd_checked = True
        for pest in pests_current:
            pest_name_list.append(pest.pest_name)
        if pest_name_list:
            pest_tbd_checked = False
        # set the update form with the current db values
        form = PlantAddUpdateForm(initial={ 'status'            : plant.status,
                                            'commonName'        : plant.commonName,
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
                                            'davis_trees'       : plant.davis_trees,
                                            'sunset_z14'        : plant.sunset_z14,
                                            'sun_exposure'      : sun_exposure_list,
                                            'water_rqmts'       : plant.water_rqmts,
                                            'pH_min'            : plant.pH_min,
                                            'pH_max'            : plant.pH_max,
                                            'soil_type'         : soil_type_list,
                                            'heat_tolerance'    : plant.heat_tolerance,
                                            'deer_resistance'   : plant.deer_resistance,
                                            'usda_zone_max'     : plant.usda_zone_max,
                                            'usda_zone_min'     : plant.usda_zone_min,
                                            'sunset_zones'      : plant.sunset_zones,
                                            'description'       : plant.description,
                                            'pruning'           : plant.pruning,
                                            'pruning_video'     : plant.pruning_video,
                                            'fertilization'     : plant.fertilization,
                                            'propagation'       : plant.propagation,
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
                                            'subspecies'        : plant.subspecies,
                                            'variety'           : plant.variety,
                                            'cultivar'          : plant.cultivar,
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
                                            'status'            : plant.status,
                                        })
        context = { 'plant'            : plant, 
                    'pests'            : pests,
                    'pest_name_list'   : pest_name_list,
                    'pest_tbd_checked' : pest_tbd_checked,
                    'form'             : form,
                    'usda_zones_opt'   : usda_zones_opt,
                    'sunset_zones_opt' : sunset_zones_opt }
        return render(request, 'plants/plant_edit.html', context)

def plant_comment(request, id):
    """ Associate a comment to a plant """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    plant = Plant.objects.get(id=id)
    comment = Comment()
    if request.method == "POST":
        form = PlantCommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment.author  = request.user.username            #
            comment.subject = form.cleaned_data.get("subject") #
            comment.comment = form.cleaned_data.get("comment") #
            comment.plant = plant                              # link the comment to the specific plant
            comment.save()
        return HttpResponseRedirect(reverse('plants:plant_details', args=(plant.id,))) 
    else:
        return HttpResponseRedirect(reverse('general:index'))
    
def plant2garden(request, id):
    """ Add a plant to a garden """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    plant = Plant.objects.get(id=id)
    garden = Garden.objects.get(owner = request.user.username)
    # Associate the plant to the user's garden
    plant.gardens.add(garden)                    
    return HttpResponseRedirect(reverse('plants:plants_summary'))

def plant_delete(request, id):
    """ Delete selected plant from the Plant database table """
    if not request.user.groups.filter(name='Editor').exists():
        return HttpResponseRedirect(reverse('general:index'))
    plant = Plant.objects.get(id=id)
    if request.method == "POST":
        # Check for and delete audio file
        if (plant.audio_name):
            plant.audio_name.delete(save=False)
        # Check for and delete image files
        if (plant.image_1):
            plant.image_1.delete(save=False)
        if (plant.image_2):
            plant.image_2.delete(save=False)
        if (plant.image_3):
            plant.image_3.delete(save=False)
        if (plant.image_4):
            plant.image_4.delete(save=False)
        # AR: Once 'My Plants' images are implemented, delete any associated 'My Plants' images

        # Delete the plant
        plant.delete()
        return HttpResponseRedirect(reverse('plants:plants_summary')) 
    else:
        context = {'plant': plant}
        return render(request, 'plants/plant_delete_modal.html', context)

def column_chooser(request):
    """ Capture the columns that the user wants to display in the plant table """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    
    # Obtain the user's saved configuration information
    user_info = request.user.userinfo

    if request.method == "POST":
        form = ColumnChooserForm(request.POST)
        if form.is_valid():
            column_selection = form.cleaned_data.get('column_selection')
            # Associate the column selection to the user's garden
            user_info.column_selection = column_selection
            user_info.save()
        else:
            return HttpResponseRedirect(reverse('plants:summary')) 
        return HttpResponseRedirect(reverse('plants:plants_summary'))
    
    else:
        column_selection = user_info.column_selection
        # convert string-based list (retrieved from db) to true Python lists
        column_selection_list  = string2list(column_selection)
        form = ColumnChooserForm(initial = {'column_selection' : column_selection_list})
        context = {'form' : form }
        return render(request, 'plants/column_chooser_modal.html', context)