# /app/myplants/views.py

import string, copy, math, json, random, base64

from django.core.mail import send_mail
from django.core.files.base import ContentFile
 
from django.http      import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.shortcuts import render, redirect # Added for images
from django.template  import loader
from django.urls      import reverse
from django.db.models import Q # used to create complex database queries that involve logical operators such as OR, AND, and NOT
from django.conf      import settings
from django.contrib   import messages

from .models          import MyPlant, MyPlantLog, MyPlantToDo, MyPlantComment
from plants.models    import Plant

from .forms  import MyPlantAddUpdateForm, MyPlantLogForm, MyPlantToDoForm, MyPlantCommentForm, MyColumnChooserForm

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

def index(request):
    """ Render the landing page for Gateway Gardens app """
    return render(request, 'general/index.html')

#

def myplants_summary(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    
    # Obtain the user's saved configuration information
    user_info = request.user.userinfo
    
    #-----------------------------------------------------------------------------------------------------
    # Executed when search request is submitted
    #-----------------------------------------------------------------------------------------------------
    if request.method == 'POST':
        # Get the search criteria from the "http request"
        # Plant Characteristics
        common_name_search      = request.POST["common_name_search"]
        genus_search            = request.POST["genus_search"]
        species_search          = request.POST["species_search"]
        type_x_search           = request.POST["type_x_search"]
        bloom_color_search      = request.POST["bloom_color_search"]
        bloom_season_search     = request.POST["bloom_season_search"]
        bloom_month_search      = request.POST["bloom_month_search"]
        pollinators_search      = request.POST["pollinators_search"]
        ca_native_search        = request.POST["ca_native_search"]
        ucd_all_star_search     = request.POST["ucd_all_star_search"]
        davis_trees_search      = request.POST["davis_trees_search"]
        sunset_z14_search       = request.POST["sunset_z14_search"]
        # Plant Requirements
        sun_exposure_search     = request.POST["sun_exposure_search"]
        water_rqmts_search      = request.POST["water_rqmts_search"]
        soil_type_search        = request.POST["soil_type_search"]
        pH_search               = request.POST["pH_search"]
        heat_tolerance_search   = request.POST["heat_tolerance_search"]
        deer_resistance_search  = request.POST["deer_resistance_search"]
        usda_zone_search        = request.POST["usda_zone_search"]
        sunset_zone_search      = request.POST["sunset_zone_search"]
        # Garden Environment
        my_sun_exposure_search  = request.POST["my_sun_exposure_search"]
        my_water_level_search   = request.POST["my_water_level_search"]
        my_soil_type_search     = request.POST["my_soil_type_search"]
        my_happiness_search     = request.POST["my_happiness_search"]

        # Store the search criteria in the user's user_info db table
        user_info.common_name_search  = common_name_search
        user_info.genus_search        = genus_search
        user_info.species_search      = species_search
        user_info.type_x_search       = type_x_search
        user_info.bloom_color_search  = bloom_color_search
        user_info.bloom_season_search = bloom_season_search
        user_info.bloom_month_search  = bloom_month_search
        user_info.pollinators_search  = pollinators_search
        user_info.ca_native_search    = ca_native_search
        user_info.ucd_all_star_search = ucd_all_star_search
        user_info.davis_trees_search  = davis_trees_search
        user_info.sunset_z14_search   = sunset_z14_search
        user_info.sun_exposure_search = sun_exposure_search
        user_info.water_rqmts_search  = water_rqmts_search
        user_info.pH_search           = pH_search
        user_info.soil_type_search    = soil_type_search
        user_info.heat_tolerance_search  = heat_tolerance_search
        user_info.deer_resistance_search = deer_resistance_search
        user_info.usda_zone_search       = usda_zone_search
        user_info.sunset_zone_search     = sunset_zone_search
        #
        user_info.my_sun_exposure_search = my_sun_exposure_search
        user_info.my_water_level_search  = my_water_level_search
        user_info.my_soil_type_search    = my_soil_type_search
        user_info.my_happiness_search    = my_happiness_search
        # Save the search criteria
        user_info.save()
    #-----------------------------------------------------------------------------------------------------
    # Executed when plants summary page is initialized
    #-----------------------------------------------------------------------------------------------------
    else:
        # Get the user's previously stored search criteria
        common_name_search      = user_info.common_name_search
        genus_search            = user_info.genus_search
        species_search          = user_info.species_search
        type_x_search           = user_info.type_x_search
        bloom_color_search      = user_info.bloom_color_search
        bloom_season_search     = user_info.bloom_season_search
        bloom_month_search      = user_info.bloom_month_search
        pollinators_search      = user_info.pollinators_search
        ca_native_search        = user_info.ca_native_search
        ucd_all_star_search     = user_info.ucd_all_star_search
        davis_trees_search      = user_info.davis_trees_search
        sunset_z14_search       = user_info.sunset_z14_search
        sun_exposure_search     = user_info.sun_exposure_search
        water_rqmts_search      = user_info.water_rqmts_search
        pH_search               = user_info.pH_search
        soil_type_search        = user_info.soil_type_search
        heat_tolerance_search   = user_info.heat_tolerance_search
        deer_resistance_search  = user_info.deer_resistance_search
        usda_zone_search        = user_info.usda_zone_search
        sunset_zone_search      = user_info.sunset_zone_search
        #
        my_sun_exposure_search  = user_info.my_sun_exposure_search
        my_water_level_search   = user_info.my_water_level_search
        my_soil_type_search     = user_info.my_soil_type_search
        my_happiness_search     = user_info.my_happiness_search
    #-----------------------------------------------------------------------------------------------------
    # Execute the search
    #-----------------------------------------------------------------------------------------------------
    # Get the user's previously stored column display sections      
    my_column_selection_list  = string2list(user_info.my_column_selection)

    # Obtain the plants that the current user has claimed for their garden
    myplants = MyPlant.objects.filter(Q(owner = request.user.username) &
                                      Q(status = 'in_my_garden')).order_by('plant__commonName')
    # Execute the search
    for myplant in myplants:
        # format multiselect attributes to remove [, ', and ]
        myplant.plant.bloom_color     = string_display(myplant.plant.bloom_color)
        myplant.plant.bloom_season    = string_display(myplant.plant.bloom_season)
        myplant.bloom_months          = string_display(myplant.plant.bloom_months)
        myplant.plant.pollinators     = string_display(myplant.plant.pollinators)
        myplant.plant.sun_exposure    = string_display(myplant.plant.sun_exposure)
        myplant.plant.water_rqmts     = string_display(myplant.plant.water_rqmts)
        myplant.plant.soil_type       = string_display(myplant.plant.soil_type)
        myplant.plant.heat_tolerance  = string_display(myplant.plant.heat_tolerance)
        myplant.plant.deer_resistance = string_display(myplant.plant.deer_resistance)
        # Create short version of usda_zones for table display
        myplant.plant.usda_zone_min = myplant.plant.usda_zone_min.split()[0]
        myplant.plant.usda_zone_max = myplant.plant.usda_zone_max.split()[0]
        # clean up the list display
        myplant.sun_exposure = string_display(myplant.sun_exposure)
        myplant.water_level  = string_display(myplant.water_level)
        myplant.soil_type    = string_display(myplant.soil_type)
        # Run through the search criteria to select the plants to show
        pH_hit = pH_check(pH_search, myplant.plant.pH_min, myplant.plant.pH_max)
        usda_zone_hit = usda_zone_check(usda_zone_search, myplant.plant.usda_zone_min, myplant.plant.usda_zone_max)
        sunset_zone_hit = sunset_zone_check(sunset_zone_search, myplant.plant.sunset_zones, sunset_zones_opt)
        bloom_month_hit = bloom_month_check(bloom_month_search, myplant.bloom_start, myplant.bloom_end, month_opt)
        if( (common_name_search      in myplant.plant.commonName) and \
            (genus_search            in myplant.plant.genus)      and \
            (species_search          in myplant.plant.species)    and \
            ((type_x_search          == myplant.plant.type_x)          or (type_x_search          == "Any")) and \
            ((bloom_color_search     in myplant.plant.bloom_color)     or (bloom_color_search     == "Any")) and \
            ((bloom_season_search    in myplant.plant.bloom_season)    or (bloom_season_search    == "Any")) and \
            ((pollinators_search     in myplant.plant.pollinators)     or (pollinators_search     == "Any")) and \
            ((ca_native_search       == myplant.plant.ca_native)       or (ca_native_search       == "Any")) and \
            ((ucd_all_star_search    == myplant.plant.ucd_all_star)    or (ucd_all_star_search    == "Any")) and \
            ((davis_trees_search     == myplant.plant.davis_trees)     or (davis_trees_search     == "Any")) and \
            ((sunset_z14_search      == myplant.plant.sunset_z14)      or (sunset_z14_search      == "Any")) and \
            ((sun_exposure_search    in myplant.plant.sun_exposure)    or (sun_exposure_search    == "Any")) and \
            ((water_rqmts_search     in myplant.plant.water_rqmts)     or (water_rqmts_search     == "Any")) and \
            ((soil_type_search       in myplant.plant.soil_type)       or (soil_type_search       == "Any")) and \
            ((heat_tolerance_search  in myplant.plant.heat_tolerance)  or (heat_tolerance_search  == "Any")) and \
            ((deer_resistance_search in myplant.plant.deer_resistance) or (deer_resistance_search == "Any")) and \
            (pH_hit)          and \
            (usda_zone_hit)   and \
            (sunset_zone_hit) and \
            (bloom_month_hit) and \
            ((my_sun_exposure_search == myplant.sun_exposure) or (my_sun_exposure_search == "Any")) and \
            ((my_water_level_search  == myplant.water_level)  or (my_water_level_search  == "Any")) and \
            ((my_soil_type_search    == myplant.soil_type)    or (my_soil_type_search    == "Any")) and \
            ((my_happiness_search    == myplant.happiness)    or (my_happiness_search    == "Any")) \
            ):
            myplant.show = "yes"
        else:
            myplant.show = "no"

    template = loader.get_template("myplants/myplants_summary.html")

    context = { 'myplants'               : myplants,
                # search field options - plant attributes
                "plant_types"            : plant_types,
                "bloom_color_opt"        : bloom_color_opt,
                "bloom_season_opt"       : bloom_season_opt,
                "pollinators_opt"        : pollinators_opt,
                "ucd_all_star_opt"       : ucd_all_star_opt,
                "davis_trees_opt"        : davis_trees_opt,
                "sunset_z14_opt"         : sunset_z14_opt,
                "ca_native_opt"          : ca_native_opt,
                # search field options - plant requirements & garden environment
                "sun_exposure_opt"       : sun_exposure_opt,
                "water_rqmts_opt"        : water_rqmts_opt,
                "soil_type_opt"          : soil_type_opt,
                "pH_opt"                 : pH_opt,
                "heat_tolerance_opt"     : heat_tolerance_opt,
                "deer_resistance_opt"    : deer_resistance_opt,
                "usda_zones_opt"         : usda_zones_opt,
                "sunset_zones_opt"       : sunset_zones_opt,
                "happiness_opt"          : happiness_opt,
                "month_opt"              : month_opt,
                # search field defaults - plant attributes
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
                # search field defaults - plant requirements
                "sun_exposure_search"    : sun_exposure_search,
                "water_rqmts_search"     : water_rqmts_search,
                "soil_type_search"       : soil_type_search,
                "pH_search"              : pH_search,
                "heat_tolerance_search"  : heat_tolerance_search,
                "deer_resistance_search" : deer_resistance_search,
                "usda_zone_search"       : usda_zone_search,
                "sunset_zone_search"     : sunset_zone_search,
                # search field defaults - my plant conditions
                "my_sun_exposure_search" : my_sun_exposure_search,
                "my_water_level_search"  : my_water_level_search,
                "my_soil_type_search"    : my_soil_type_search,
                "my_happiness_search"    : my_happiness_search,
                # table column selection
                'my_column_selection'    : my_column_selection_list, }
    return HttpResponse(template.render(context, request))

def my_column_chooser(request):
    """ Capture the columns that the user wants to display in the plant table """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    
    # Obtain the user's saved configuration information
    user_info = request.user.userinfo

    if request.POST:
        form = MyColumnChooserForm(request.POST)
        if form.is_valid():
            my_column_selection = form.cleaned_data.get('my_column_selection')
            # Associate the column selection to the user's garden
            user_info.my_column_selection = my_column_selection
            user_info.save()
        else:
            return HttpResponseRedirect(reverse('myplants:summary')) 
        return HttpResponseRedirect(reverse('myplants:myplants_summary'))
    else:
        my_column_selection = user_info.my_column_selection
        # convert string-based list (retrieved from db) to true Python lists
        my_column_selection_list  = string2list(my_column_selection)
        form = MyColumnChooserForm(initial = {'my_column_selection' : my_column_selection_list})
        context = {'form' : form }
        return render(request, 'myplants/my_column_chooser_modal.html', context)

#

def myplant_status(request, id):
    """ Set the selected plant's status  """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    #
    plant = Plant.objects.get(id=id)
    myplants = MyPlant.objects.filter(owner = request.user.username)
    if request.POST:
        my_plant_status = request.POST["my_plant_status"]

        # Cases where the user already has a my_plant associated with the plant
        for myplant in myplants:
            if myplant.plant == plant:
                if my_plant_status == "not_in_my_garden":
                    myplant.delete()
                    return HttpResponseRedirect(reverse('plants:plants_summary'))
                elif my_plant_status == 'in_my_garden':
                    return HttpResponseRedirect(reverse('myplants:myplant_update', args=(myplant.id,)))
                elif my_plant_status == 'wish_list':
                    myplant.delete()
                    myplant.plant  = plant
                    myplant.status = 'wish_list'
                    myplant.save()
                    return HttpResponseRedirect(reverse('plants:plants_summary'))
        # Cases where the user currently has no my_plant associated with the plant
        if my_plant_status == "not_in_my_garden":
            return HttpResponseRedirect(reverse('plants:plants_summary'))
        elif my_plant_status == 'in_my_garden':
            return HttpResponseRedirect(reverse('myplants:myplant_add', args=(plant.id,)))
        elif my_plant_status == 'wish_list':
            myplant = MyPlant()
            myplant.plant  = plant
            myplant.status = 'wish_list'
            myplant.owner  = request.user.username
            myplant.save()
            return HttpResponseRedirect(reverse('plants:plants_summary'))
        return HttpResponseRedirect(reverse('plants:plants_summary')) 
    else:
        # Find my current status (if one exists) for the plant
        status = "not_in_my_garden"
        for myplant in myplants:
            if myplant.plant == plant:
                status = myplant.status
        context = { 'plant'  : plant,
                    'status' : status, }
        return render(request, 'myplants/myplant_status_modal.html', context)
    
def myplant_add(request, id):
    """ Associate a 'plant' to 'myplant' """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    plant = Plant.objects.get(id=id)
    myplant = MyPlant()
    if request.POST:
        form = MyPlantAddUpdateForm(request.POST)
        if form.is_valid():
            myplant.owner        = request.user.username                 #
            myplant.date_planted = form.cleaned_data.get("date_planted") #
            myplant.location     = form.cleaned_data.get("location")     #
            myplant.sun_exposure = form.cleaned_data.get("sun_exposure") #
            myplant.water_level  = form.cleaned_data.get("water_level")  #
            myplant.soil_type    = form.cleaned_data.get("soil_type")    #
            myplant.pH           = form.cleaned_data.get("pH")           #
            myplant.bloom_color  = form.cleaned_data.get("bloom_color")  #
            myplant.bloom_start  = form.cleaned_data.get("bloom_start")  #
            myplant.bloom_end    = form.cleaned_data.get("bloom_end")    #
            myplant.happiness    = form.cleaned_data.get("happiness")    #
            myplant.notes        = form.cleaned_data.get("notes")        #
            myplant.plant        = plant                                 # link myplant to the specific plant
            # Build list of bloom months
            myplant.bloom_months = bloom_month_list(myplant.bloom_start, myplant.bloom_end, month_opt) 
            # Set plant status to "in my garden"  
            myplant.status = 'in_my_garden'
            myplant.save()
        return HttpResponseRedirect(reverse('plants:plants_summary')) 
    else:
        form = MyPlantAddUpdateForm()
        context = { 'plant' : plant,
                    'form'  : form }
        return render(request, 'myplants/myplant_add.html', context)
    
def myplant_update(request, id):
    """ Update details related a specific My Plant """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    myplant = MyPlant.objects.get(id=id)
    plant   = Plant.objects.get(id=myplant.plant.id)
    if request.POST:
        form = MyPlantAddUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            myplant.date_planted = form.cleaned_data.get("date_planted") #
            myplant.location     = form.cleaned_data.get("location")     #
            myplant.sun_exposure = form.cleaned_data.get("sun_exposure") #
            myplant.water_level  = form.cleaned_data.get("water_level")  #
            myplant.soil_type    = form.cleaned_data.get("soil_type")    #
            myplant.pH           = form.cleaned_data.get("pH")           #
            myplant.bloom_color  = form.cleaned_data.get("bloom_color")  #
            myplant.bloom_start  = form.cleaned_data.get("bloom_start")  #
            myplant.bloom_end    = form.cleaned_data.get("bloom_end")    #
            myplant.happiness    = form.cleaned_data.get("happiness")    #
            myplant.notes        = form.cleaned_data.get("notes")        #
            # Build list of bloom months
            myplant.bloom_months = bloom_month_list(myplant.bloom_start, myplant.bloom_end, month_opt)
            # Set plant status to "in my garden"  
            myplant.status = 'in_my_garden'   
            myplant.save()
        return HttpResponseRedirect(reverse('myplants:myplants_summary')) 
    else:
        # convert string-based lists (retrieved from db) to true Python lists
        sun_exposure_list = string2list(myplant.sun_exposure)
        water_level_list = string2list(myplant.water_level)
        # set the update form with the current db values
        form = MyPlantAddUpdateForm(initial={ 'date_planted' : myplant.date_planted,
                                              'location'     : myplant.location,
                                              'sun_exposure' : sun_exposure_list,
                                              'water_level'  : water_level_list,
                                              'soil_type'    : myplant.soil_type,
                                              'pH'           : myplant.pH,
                                              'bloom_color'  : myplant.bloom_color,
                                              'bloom_start'  : myplant.bloom_start,
                                              'bloom_end'    : myplant.bloom_end,
                                              'happiness'    : myplant.happiness,
                                              'notes'        : myplant.notes,
                                            })
        context = { 'myplant' : myplant,
                    'plant'   : plant,
                    'form'    : form }
        return render(request, 'myplants/myplant_update.html', context)

def myplant_delete(request, id):
    """ Delete selected plant from the MyPlants database table """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    myplant = MyPlant.objects.get(id=id)
    if request.POST:
        myplant.delete()
        return HttpResponseRedirect(reverse('myplants:myplants_summary')) 
    else:
        context = {'myplant': myplant}
        return render(request, 'myplants/myplant_delete_modal.html', context)

#

def myplant_details(request, id):
    """ Show a detailed view of a specific plant """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    # Uses the id to locate the correct record in the MyPlant and MyPlant tables
    myplant = MyPlant.objects.get(id=id)
    plant   = Plant.objects.get(id=myplant.plant.id)
    # format multiselect attributes to remove [, ', and ]
    myplant.sun_exposure  = string_display(myplant.sun_exposure)
    myplant.soil_type     = string_display(myplant.soil_type)
    plant.bloom_color     = string_display(plant.bloom_color)
    plant.bloom_season    = string_display(plant.bloom_season)
    plant.pollinators     = string_display(plant.pollinators)
    plant.sun_exposure    = string_display(plant.sun_exposure)
    plant.water_rqmts     = string_display(plant.water_rqmts)
    plant.soil_type       = string_display(plant.soil_type)
    plant.heat_tolerance  = string_display(plant.heat_tolerance)
    plant.deer_resistance = string_display(plant.deer_resistance)
    # get all log entries related to the plant                
    myplant_logs          = MyPlantLog.objects.filter(myplant__pk=id) 
    # get all To Do items related to the plant
    myplant_todos         = MyPlantToDo.objects.filter(myplant__pk=id)
    # get all comments related to the plant                
    myplant_comments      = MyPlantComment.objects.filter(myplant__pk=id) 
    # Obtain the user's saved configuration information
    user_info = request.user.userinfo
    template = loader.get_template("myplants/myplant_details.html")
    # Specify the two input forms that exist on the page modals
    # Prefixes are necessary for the Quill forms to work correctly
    log_add_form = MyPlantLogForm(prefix='log_add_form')
    comment_form = MyPlantCommentForm(prefix='comment_form')
    context  = { "user_info"        : user_info,
                 "myplant"          : myplant, 
                 "plant"            : plant,
                 "myplant_logs"     : myplant_logs,
                 "myplant_todos"    : myplant_todos,
                 "myplant_comments" : myplant_comments,
                 "log_add_form"     : log_add_form,
                 "comment_form"     : comment_form, 
               }
    # Send "context" to template and output the html from the template
    return HttpResponse(template.render(context, request)) 

def myplant_log_add(request, id):
    """ Add My Plant Log Entry """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    
    myplant     = MyPlant.objects.get(id=id)
    myplant_log = MyPlantLog()
    if request.POST:
        log_add_form = MyPlantLogForm(request.POST, request.FILES, prefix='log_add_form')
        if log_add_form.is_valid():
            myplant_log.author  = request.user.username
            myplant_log.subject = log_add_form.cleaned_data.get("log_subject")
            myplant_log.date    = log_add_form.cleaned_data.get("log_date")
            myplant_log.entry   = log_add_form.cleaned_data.get("log_entry")
            # Process images
            if 'log_image_1' in request.FILES:
                myplant_log.image_1 = request.FILES['log_image_1']
            else:
                myplant_log.caption_1 = log_add_form.cleaned_data.get('log_caption_1')
            if 'log_image_2' in request.FILES:
                myplant_log.image_2 = request.FILES['log_image_2']
            myplant_log.caption_2 = log_add_form.cleaned_data.get('log_caption_2')
            if 'log_image_3' in request.FILES:
                myplant_log.image_3 = request.FILES['log_image_3']
            myplant_log.caption_3 = log_add_form.cleaned_data.get('log_caption_3')
            if 'log_image_4' in request.FILES:
                myplant_log.image_4 = request.FILES['log_image_4']
            myplant_log.caption_4 = log_add_form.cleaned_data.get('log_caption_4')
            
            # link the log entry to the specific plant
            myplant_log.myplant = myplant                          
            myplant_log.save()

            response_data = {
                'status': 'success',
                'message': '<p>Processed log entry successfully</p>',
            }
        return JsonResponse(response_data)
    else:
        return HttpResponseRedirect(reverse('general:index'))

def myplant_log_edit(request, id):
    """ Edit My Plant Log Entry item"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    # Get the Log item to be edited
    myplant_log = MyPlantLog.objects.get(id=id)
    # Edit the To Do item
    if request.POST:
        log_edit_form = MyPlantLogForm(request.POST, request.FILES, prefix='log_edit_form')
        if log_edit_form.is_valid():
            myplant_log.subject = log_edit_form.cleaned_data.get("log_subject")
            myplant_log.date    = log_edit_form.cleaned_data.get("log_date")
            myplant_log.entry   = log_edit_form.cleaned_data.get("log_entry")
            # Process images
            if 'log_image_1' in request.FILES:
                if (myplant_log.image_1):
                    myplant_log.image_1.delete(save=False)
                myplant_log.image_1 = request.FILES['log_image_1']
            myplant_log.caption_1 = log_edit_form.cleaned_data.get('log_caption_1')
            if 'log_image_2' in request.FILES:
                if (myplant_log.image_2):
                    myplant_log.image_2.delete(save=False)
                myplant_log.image_2 = request.FILES['log_image_2']
            myplant_log.caption_2 = log_edit_form.cleaned_data.get('log_caption_2')
            if 'log_image_3' in request.FILES:
                if (myplant_log.image_3):
                    myplant_log.image_3.delete(save=False)
                myplant_log.image_3 = request.FILES['log_image_3']
            myplant_log.caption_3 = log_edit_form.cleaned_data.get('log_caption_3')
            if 'log_image_4' in request.FILES:
                if (myplant_log.image_4):
                    myplant_log.image_1.delete(save=False)
                myplant_log.image_4 = request.FILES['log_image_4']
            myplant_log.caption_4 = log_edit_form.cleaned_data.get('log_caption_4')
            myplant_log.save()
            response_data = {
                'status': 'success',
                'message': '<p>Processed log entry successfully</p>',
            }
        return JsonResponse(response_data)
    # Populate the edit modal fields and render the modal
    else:
        log_edit_form = MyPlantLogForm(prefix='log_edit_form',
                                       initial = { 'log_subject'   : myplant_log.subject,
                                                   'log_entry'     : myplant_log.entry,
                                                   'log_date'      : myplant_log.date,
                                                   'log_image_1'   : myplant_log.image_1,
                                                   'log_caption_1' : myplant_log.caption_1,
                                                   'log_image_2'   : myplant_log.image_2,
                                                   'log_caption_2' : myplant_log.caption_2,
                                                   'log_image_3'   : myplant_log.image_3,
                                                   'log_caption_3' : myplant_log.caption_3,
                                                   'log_image_4'   : myplant_log.image_4, 
                                                   'log_caption_4' : myplant_log.caption_4,
                                                   'quill_delta'   : myplant_log.entry.delta,
                                                   'quill_html'    : myplant_log.entry.html
                                                   })
        context = { 'myplant_log'   : myplant_log,
                    'log_edit_form' : log_edit_form }
        return render(request, 'myplants/myplant_log_edit_modal.html', context)

def myplant_log_del(request, id):
    """ Delete My Plant Log Entry item"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    # Get to Log item to be deleted
    myplant_log = MyPlantLog.objects.get(id=id)
    # Delete the To Do item
    if request.POST:
        myplant_log.delete()
        return HttpResponseRedirect(reverse('myplants:myplant_details', args=(myplant_log.myplant.id,)))
    # Populate the delete modal fields and render the modal
    else:
        context = { 'myplant_log' : myplant_log }
        return render(request, 'myplants/myplant_log_del_modal.html', context)

def myplant_todo_add(request, id):
    """ Add My Plant To Do item """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    myplant      = MyPlant.objects.get(id=id)
    myplant_todo = MyPlantToDo()
    if request.POST:
        form = MyPlantToDoForm(request.POST, request.FILES)
        if form.is_valid():
            myplant_todo.owner    = request.user.username
            myplant_todo.complete = False
            myplant_todo.date     = form.cleaned_data.get("todo_date")
            myplant_todo.action   = form.cleaned_data.get("todo_action")
            myplant_todo.details  = form.cleaned_data.get("todo_details")
            myplant_todo.repeat   = form.cleaned_data.get("todo_repeat")
            # link the To Do item to the specific plant
            myplant_todo.myplant = myplant
            myplant_todo.save()
        return HttpResponseRedirect(reverse('myplants:myplant_details', args=(myplant.id,))) 
    else:
        context = { 'myplant'         : myplant,
                    'todo_action_opt' : todo_action_opt,
                    'todo_repeat_opt' : todo_repeat_opt,
                  }
        return render(request, 'myplants/myplant_todo_add_modal.html', context)
    
def myplant_todo_edit(request, id):
    """ Edit My Plant To Do item """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    # Get To Do item to be edited
    myplant_todo = MyPlantToDo.objects.get(id=id)
    #
    if request.POST:
        form = MyPlantToDoForm(request.POST, request.FILES)
        if form.is_valid():
            myplant_todo.date     = form.cleaned_data.get("todo_date")
            myplant_todo.action   = form.cleaned_data.get("todo_action")
            myplant_todo.details  = form.cleaned_data.get("todo_details")
            myplant_todo.repeat   = form.cleaned_data.get("todo_repeat")
            myplant_todo.save()
        return HttpResponseRedirect(reverse('myplants:myplant_details', args=(myplant_todo.myplant.id,)))
    # Populate the edit modal fields and render the modal
    else:
        context = {     
                    'myplant_todo'    : myplant_todo,
                    'todo_action_opt' : todo_action_opt,
                    'todo_repeat_opt' : todo_repeat_opt,
                    'todo_date'       : myplant_todo.date,
                    'todo_action'     : myplant_todo.action,
                    'todo_details'    : myplant_todo.details,
                    'todo_repeat'     : myplant_todo.repeat 
                  }
        return render(request, 'myplants/myplant_todo_edit_modal.html', context)
    
def myplant_todo_del(request, id):
    """ Delete My Plant To Do item"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    # Get to To Do item to be deleted
    myplant_todo = MyPlantToDo.objects.get(id=id)
    # Delete the To Do item
    if request.POST:
        myplant_todo.delete()
        return HttpResponseRedirect(reverse('myplants:myplant_details', args=(myplant_todo.myplant.id,)))
    # Populate the delete modal fields and render the modal
    else:
        context = { 'myplant_todo' : myplant_todo }
        return render(request, 'myplants/myplant_todo_del_modal.html', context)
    
def myplant_todo_done(request, id):
    """ My Plant To Do item - toggle conpletion status """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    # Get the To Do item to have completion status toggled
    myplant_todo = MyPlantToDo.objects.get(id=id)
    if request.method == 'POST':
        # Parses the JSON data from the request body
        data_JSON = json.loads(request.body)
        
        if(myplant_todo.complete == True):
            myplant_todo.complete = False
        else:
            myplant_todo.complete = True
        myplant_todo.save()
        # return JsonResponse({'test' : 'test' })
        return HttpResponseRedirect(reverse('myplants:myplant_details', args=(myplant_todo.myplant.id,)))

def myplant_todo_save(request, id):
    """ My Plant To Do items - save sort column and direction """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    user_info = request.user.userinfo
    if request.method == 'POST':

        # Parses the JSON data from the request body
        data_JSON_string = request.body.decode('utf-8')
        # Convert the JSON string into a dictionary
        data_dict= json.loads(data_JSON_string)

        # Get the sort parameters and save to db
        user_info.lastToDoSortCol = data_dict["lastToDoSortCol"]
        user_info.lastToDoSortDir = data_dict["lastToDoSortDir"]
        user_info.save()
        
    return JsonResponse({'test' : 'test' })

def myplant_comment(request, id):
    """ Associate a comment to a plant """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    myplant         = MyPlant.objects.get(id=id)
    myplant_comment = MyPlantComment()
    if request.POST:
        comment_form = MyPlantCommentForm(request.POST, request.FILES, prefix='comment_form')
        if comment_form.is_valid():
            myplant_comment.author  = request.user.username            #
            myplant_comment.subject = comment_form.cleaned_data.get("subject") #
            myplant_comment.comment = comment_form.cleaned_data.get("comment") #
            myplant_comment.myplant = myplant                          # link the comment to the specific plant
            myplant_comment.save()
        return HttpResponseRedirect(reverse('myplants:myplant_details', args=(myplant.id,))) 
    else:
        return HttpResponseRedirect(reverse('general:index'))
