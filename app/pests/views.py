# app/pests/views.py

from django.contrib.auth.decorators import login_required, user_passes_test
from django.http        import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.shortcuts   import render, get_object_or_404
from django.template    import loader
from django.urls        import reverse
from core_utils.helpers import login_required_no_next, is_garden_editor
from pests.models       import Pest
from pests.forms        import PestAddUpdateForm

@login_required_no_next
def pest_summary(request):
    """ Render the page to show all pests for Gateway Gardens app """
    pests = Pest.objects.all().order_by('pest_type', 'pest_name')
    return render(request, 'pests/pest_summary.html', {'pests': pests})

@login_required_no_next
def pest_details(request, id):
    """ Show a detailed view of a specific pest """
    # Check to see if the id points to a valid pest
    pest = get_object_or_404(Pest, id=id)
    
    # Dynamically package image and caption attributes
    # Pack only valid/existing images to save memory and avoid template rendering bugs
    image_fields = []
    for i in range(1, 5):
        image_file = getattr(pest, f'image_{i}', None)
        if image_file:  # Only append if an image actually exists in this slot
            image_fields.append({
                'index': i,
                'image_file': image_file,
                'caption_value': getattr(pest, f'caption_{i}', ''),
            })

    context = { "pest"         : pest, 
                "image_fields" : image_fields, }
    return render(request, 'pests/pest_details.html', context)

@login_required_no_next
@user_passes_test(is_garden_editor, login_url='general:index', redirect_field_name=None)
def pest_add(request):
    """ Render the page to add pests to the database for Gateway Gardens app """
  
    # Create a new pest and save it to obtain an ID
    pest = Pest()
    pest.save()
    # Give the new pest a default common name and status
    pest.pest_name = "< New Pest " + str(pest.id) + " >"
    pest.save()
    # Edit the newly created pest
    return HttpResponseRedirect(reverse('pests:pest_edit', args=(pest.id,))) 

@login_required_no_next
@user_passes_test(is_garden_editor, login_url='general:index', redirect_field_name=None)
def pest_edit(request, id):
    """ Render the page to add pests to the database for Gateway Gardens app """

    pest = Pest.objects.get(id=id)
    image_quantity = 4

    if request.method == "POST":
        form = PestAddUpdateForm(request.POST)
        if form.is_valid():
            pest.pest_name   = form.cleaned_data.get('pest_name')
            pest.family      = form.cleaned_data.get('family')
            pest.genus       = form.cleaned_data.get('genus')
            pest.species     = form.cleaned_data.get('species')
            pest.pest_type   = form.cleaned_data.get('pest_type')
            pest.life_cycle  = form.cleaned_data.get('life_cycle')
            pest.pest_url    = form.cleaned_data.get('pest_url')
            pest.description = form.cleaned_data.get('description')
            pest.management  = form.cleaned_data.get('management') 
            # Loop through the images - check for new image - if yes, delete any existing image
            for i in range(1, image_quantity + 1):
                image_attr   = f'image_{i}'
                caption_attr = f'caption_{i}'
                # Handle the image replacement and old file deletion
                if image_attr in request.FILES:
                    existing_image = getattr(pest, image_attr)
                    if existing_image:
                        existing_image.delete(save=False)
                    setattr(pest, image_attr, request.FILES[image_attr])
                # Update the caption
                setattr(pest, caption_attr, form.cleaned_data.get(caption_attr))
            # Save the thumbnail image
            if 'image_1' in request.FILES:
                if (pest.pest_thumbnail):
                    pest.pest_thumbnail.delete(save=False)
                pest.pest_thumbnail = request.FILES['image_1']
            pest.save()

        response_data = {
            'status': 'success',
            'message': f'Edited pest successfully',
        }
        return JsonResponse(response_data)
    else:
        template = loader.get_template('pests/pest_edit.html')
        # set the edit form with the current db values
        form = PestAddUpdateForm(initial = { 'pest_name'   : pest.pest_name,
                                             'family'      : pest.family,
                                             'genus'       : pest.genus,
                                             'species'     : pest.species,
                                             'pest_type'   : pest.pest_type,
                                             'life_cycle'  : pest.life_cycle,
                                             'pest_url'    : pest.pest_url,
                                             'description' : pest.description,
                                             'management'  : pest.management,
                                           })
        # Dynamically package image and caption attributes
        image_fields = []
        for i in range(1, image_quantity + 1):
            image_fields.append(
            {
                'index'        : i,
                'image_file'   : getattr(pest, f'image_{i}', None),
                'caption_value': getattr(pest, f'caption_{i}', ''),
                'form_image'   : form[f'image_{i}'],
                'form_caption' : form[f'caption_{i}'],
            })
        context = { 'pest'           : pest,
                    'form'           : form,
                    'image_fields'   : image_fields, 
                    'image_quantity' : image_quantity, }
        return HttpResponse(template.render(context, request ))
  
@login_required_no_next
@user_passes_test(is_garden_editor, login_url='general:index', redirect_field_name=None)
def pest_delete(request, id):
    """ Delete selected pest from the Pest database table """
    
    # Check to see if the id points to a valid pest
    pest = get_object_or_404(Pest, id=id)
    
    if request.method == "POST":
        pest.delete()
        return HttpResponseRedirect(reverse('pests:pest_summary'))             
    else:
        context = {'pest': pest}
        return render(request, 'pests/pest_delete_modal.html', context)
