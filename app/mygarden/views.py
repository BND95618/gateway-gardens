# app/mygarden/views.py

import json

from django.http      import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.shortcuts import render
from django.template  import loader
from django.urls      import reverse

from mygarden.models  import Garden
from plants.models    import Plant, MyPlant, MyPlantToDo

from mygarden.forms   import GardenAddUpdateForm

todo_action_opt  = ["Fertilize", "Harvest", "Mow", "Plant", "Prune", "Spray", "Other"]
todo_repeat_opt  = ["Daily", "Weekly", "Bi-Weekly", "Monthly", "Yearly", "Never"]
status_opt       = ["Development", "Review", "Published", "Archived"]

def mygarden_summary(request):
    """ Render the individual user's garden summary for Gateway Gardens app """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    garden = Garden.objects.get(owner = request.user.username)
    template = loader.get_template("mygarden/mygarden_summary.html")
    image_fields   = []
    image_quantity = 8
    # Dynamically package image and caption attributes
    for i in range(1, image_quantity + 1):
        image_fields.append(
        {
            'index'        : i,
            'image_file'   : getattr(garden, f'image_{i}', None),
            'caption_value': getattr(garden, f'caption_{i}', ''),
        })
    context = { "garden"       : garden,
                "image_fields" : image_fields, } 
    return HttpResponse(template.render(context, request))

def mygarden_add(request):
    """ Add garden to the database """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    garden = Garden()
    garden.name = request.user.username + "'s Garden"
    garden.save()
    # Edit the newly created garden
    return HttpResponseRedirect(reverse('mygarden:mygarden_edit', args=(garden.id,))) 

def mygarden_edit(request, id):
    """ Update garden details """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    garden = Garden.objects.get(id=id)
    image_quantity = 8

    if request.POST:
        form = GardenAddUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            garden.owner       = request.user.username
            garden.name        = form.cleaned_data.get('name')
            garden.city        = form.cleaned_data.get('city')
            garden.state       = form.cleaned_data.get('state')
            garden.usda_zone   = form.cleaned_data.get('usda_zone')
            garden.sunset_zone = form.cleaned_data.get('sunset_zone')
            garden.description = form.cleaned_data.get('description')
            # Loop through the images
            for i in range(1, image_quantity+1):
                image_attr   = f'image_{i}'
                caption_attr = f'caption_{i}'
                # Handle the image replacement and old file deletion
                if image_attr in request.FILES:
                    existing_image = getattr(garden, image_attr)
                    if existing_image:
                        existing_image.delete(save=False)
                    setattr(garden, image_attr, request.FILES[image_attr])
                # Update the caption
                setattr(garden, caption_attr, form.cleaned_data.get(caption_attr))
            # Save the updated garden information
            garden.save()

        response_data = {
            'status': 'success',
            'message': f'Received audio successfully',
        }
        return JsonResponse(response_data)
    else:
        # set the edit form with the current db values
        form = GardenAddUpdateForm(initial={ 'name'        : garden.name,
                                             'city'        : garden.city,
                                             'state'       : garden.state,
                                             'usda_zone'   : garden.usda_zone,
                                             'sunset_zone' : garden.sunset_zone,
                                           })
        # Dynamically package image and caption attributes
        image_fields = []
        for i in range(1, image_quantity + 1):
            image_fields.append(
            {
                'index'        : i,
                'image_file'   : getattr(garden, f'image_{i}', None),
                'caption_value': getattr(garden, f'caption_{i}', ''),
                'form_image'   : form[f'image_{i}'],
                'form_caption' : form[f'caption_{i}'],
            })
        context = { 'garden'       : garden, 
                    'form'         : form,
                    'image_fields' : image_fields,
                  }
        return render(request, 'mygarden/mygarden_edit.html', context)
 
def mygarden_plan(request):
    """ Render the Garden Plan page """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    # Obtain the user's saved configuration information
    user_info = request.user.userinfo
    plants = Plant.objects.all()
    if request.method == 'POST':
        # Parses the JSON data from the request body
        shapes_JSON = json.loads(request.body)
        # Save the garden design to db
        user_info.shapes_JSON = shapes_JSON
        user_info.save()
        # AR: return without sending data back
        shapes_JSON = json.dumps(user_info.shapes_JSON)
        return JsonResponse({'shapes_JSON' : shapes_JSON})
    else:
        shapes_JSON = json.dumps(user_info.shapes_JSON)
        context = { 'plants'      : plants,
                    'shapes_JSON' : shapes_JSON }
        return render(request, 'mygarden/mygarden_plan.html', context)

def mygarden_plan_edit_modal(request):
    """ Display shape edit menu in a pop-up modal """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    
    if request.method == 'POST':
        # Get the JSON sring with the selected shape attributes
        shape_JSON_string = request.body.decode('utf-8')
        # Convert the JSON string into a dictionary
        shape_dict = json.loads(shape_JSON_string)

        context = { "x"      : shape_dict["x"],
                    "y"      : shape_dict["y"],
                    "width"  : shape_dict["width"],
                    "height" : shape_dict["height"],
                  }
        return render(request, 'mygarden/mygarden_plan_edit_modal.html', context)
    else:
        print("INFO: Error!")
        return HttpResponseRedirect(reverse('plants:index'))
 
def plant_details_modal(request):
    """ Display plant detail in a pop-up modal """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    
    if request.method == 'POST':
        # Get the JSON sring with the common name of the requested plant
        requestedPlant_json_string = request.body.decode('utf-8')
        # Convert the JSON string into a dictionary
        requestedPlant_dict = json.loads(requestedPlant_json_string)
        # Get the Common Name of the plant requested
        requestedPlant = requestedPlant_dict["requestedPlant"]
        # Retrieve the requested plant from the db
        plant = Plant.objects.get(commonName = requestedPlant)

        plant.sun_exposure    = string_display(plant.sun_exposure)
        plant.water_rqmts     = string_display(plant.water_rqmts)
        plant.bloom_color     = string_display(plant.bloom_color)
        plant.bloom_season    = string_display(plant.bloom_season)
        plant.pollinators     = string_display(plant.pollinators)
        plant.soil_type       = string_display(plant.soil_type)
        plant.heat_tolerance  = string_display(plant.heat_tolerance)
        plant.deer_resistance = string_display(plant.deer_resistance)

        context = { "plant" : plant }
        return render(request, 'mygarden/plant_details_modal.html', context)
    else:
        print("INFO: Error!")
        return HttpResponseRedirect(reverse('plants:index'))
 
def plant_fetch(request):
    """ """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))

    if request.method == 'POST':
        # Get the JSON sring with the common name of the requested plant
        requestedPlant_json_string = request.body.decode('utf-8')
        # Convert the JSON string into a dictionary
        requestedPlant_dict = json.loads(requestedPlant_json_string)
        # Get the Common Name of the plant requested
        requestedPlant = requestedPlant_dict["requestedPlant"]
        # Retrieve the requested plant from the db and convert to a dictionary
        plant_json = list(Plant.objects.filter(commonName = requestedPlant).values())
        # safe=False is needed if returning a list directly
        return JsonResponse(plant_json, safe=False)
    else:
        print("INFO: Error!")
        return HttpResponseRedirect(reverse('plants:index'))

def mygarden_todo(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    template = loader.get_template("mygarden/mygarden_todo.html")
    # Obtain the user's saved configuration information
    user_info = request.user.userinfo
    # Obtain the user's garden
    myGarden = Garden.objects.get(owner = request.user.username)
    # Obtain all of the To Do items for the current user and sort by date
    mygarden_todos = MyPlantToDo.objects.filter(owner = request.user.username).order_by('date')
    context = { 'user_info'     : user_info,
                'myGarden'      : myGarden,
                "mygarden_todo" : mygarden_todos, }
    return HttpResponse(template.render(context, request))

def mygarden_todo_details(request, id):
    """  My Plant To Do item details modal """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    
    myplant_todo = MyPlantToDo.objects.get(id=id)
    context = { 'myplant_todo' : myplant_todo }
    return render(request, 'mygarden/mygarden_todo_details_modal.html', context)   

def mygarden_todo_add(request, id):
    """ Add My Plant To Do item """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    
    if request.POST:
        myplant_todo = MyPlantToDo()

        common_name   = request.POST["common_name"]
        myplants = MyPlant.objects.filter(owner = request.user.username)
        for myplant in myplants:
            if myplant.plant.commonName == common_name:
                myplant_todo.myplant = myplant
        # Get the rest of the To Do item attributes
        myplant_todo.owner    = request.user.username
        myplant_todo.complete = False
        myplant_todo.date     = request.POST["todo_date"]
        myplant_todo.action   = request.POST["todo_action"]
        myplant_todo.repeat   = request.POST["todo_repeat"]
        myplant_todo.details  = request.POST["todo_details"]
        
        myplant_todo.save()

        return HttpResponseRedirect(reverse('mygarden:mygarden_todo'))
    else:
        myGarden = Garden.objects.get(id=id)
        myPlants = MyPlant.objects.filter(owner = request.user.username)
        context = { 'myGarden'        : myGarden,
                    'myPlants'        : myPlants,
                    'todo_action_opt' : todo_action_opt,
                    'todo_repeat_opt' : todo_repeat_opt,
                  }
        return render(request, 'mygarden/mygarden_todo_add_modal.html', context)
    
def mygarden_todo_edit(request, id):
    """ edit My Plant To Do item """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    
    myplants     = MyPlant.objects.filter(owner = request.user.username)
    myplant_todo = MyPlantToDo.objects.get(id=id)

    if request.POST:
        common_name = request.POST["common_name"]
        for myplant in myplants:
            if myplant.plant.commonName == common_name:
                myplant_todo.myplant = myplant
        # Get the rest of the To Do item attributes
        myplant_todo.owner    = request.user.username
        myplant_todo.complete = False
        myplant_todo.date     = request.POST["todo_date"]
        myplant_todo.action   = request.POST["todo_action"]
        myplant_todo.repeat   = request.POST["todo_repeat"]
        myplant_todo.details  = request.POST["todo_details"]
        myplant_todo.save()
        return HttpResponseRedirect(reverse('mygarden:mygarden_todo'))
    else:
        context = { 'myplants'        : myplants,
                    'myplant_todo'    : myplant_todo,
                    'todo_action_opt' : todo_action_opt,
                    'todo_repeat_opt' : todo_repeat_opt,
                  }
        return render(request, 'mygarden/mygarden_todo_edit_modal.html', context)    
    
def mygarden_todo_del(request, id):
    """ Delete My Plant To Do item"""
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    # Get to To Do item to be deleted
    myplant_todo = MyPlantToDo.objects.get(id=id)
    # Delete the To Do item
    if request.POST:
        myplant_todo.delete()
        return HttpResponseRedirect(reverse('mygarden:mygarden_todo',))
    # Populate the delete modal fields and render the modal
    else:
        context = { 'myplant_todo' : myplant_todo }
        return render(request, 'mygarden/mygarden_todo_del_modal.html', context)

def mygarden_todo_done(request, id):
    """ My Plant To Do item - toggle conpletion status """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    # Get the To Do item to have completion status toggled
    myplant_todo = MyPlantToDo.objects.get(id=id)
    if request.method == 'POST':
        if(myplant_todo.complete == True):
            myplant_todo.complete = False
        else:
            myplant_todo.complete = True
        myplant_todo.save()
        return HttpResponseRedirect(reverse('myplants:myplant_details', args=(myplant_todo.myplant.id,)))

def mygarden_todo_save(request, id):
    """ My Plant To Do items - save sort column and direction """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
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

def mygarden_todo_fetch(request):
    """ My Plant To Do items - save sort column and direction """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    
    # Obtain all of the To Do items for the current user
    mygarden_todos = MyPlantToDo.objects.filter(owner = request.user.username)
    # Add the plant common name to the todo model for calendar display
    for todo in mygarden_todos:
        todo.commonName = todo.myplant.plant.commonName
        todo.pruning    = todo.myplant.plant.pruning
        todo.save() 
    # Convert queryset to a list of dictionaries
    todos = list(mygarden_todos.values()) 
    return JsonResponse(todos, safe=False)

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