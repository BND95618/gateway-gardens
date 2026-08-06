# app/pests/views.py

from django.http      import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.shortcuts import render
from django.template  import loader
from django.urls      import reverse
from pests.models     import Pest
from pests.forms      import PestAddUpdateForm

def pest_summary(request):
    """ Render the page to show all pests for Gateway Gardens app """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    pests = Pest.objects.all().order_by('pest_type', 'pest_name')
    template = loader.get_template("pests/pest_summary.html")
    context = { 'pests' : pests }
    return HttpResponse(template.render(context, request))

def pest_details(request, id):
    """ Show a detailed view of a specific plant """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    pest = Pest.objects.get(id=id)
    template = loader.get_template("pests/pest_details.html")
    context = { "pest" : pest }
    return HttpResponse(template.render(context, request))

def pest_add(request):
    """ Render the page to add pests to the database for Gateway Gardens app """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    # Create a new pest and save it to obtain an ID
    pest = Pest()
    pest.save()
    # Give the new pest a default common name and status
    pest.pest_name = "< New Pest " + str(pest.id) + " >"
    pest.save()
    # Edit the newly created pest
    return HttpResponseRedirect(reverse('pests:pest_edit', args=(pest.id,))) 

def pest_edit(request, id):
    """ Render the page to add pests to the database for Gateway Gardens app """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    pest = Pest.objects.get(id=id)
    if request.POST:
        form = PestAddUpdateForm(request.POST)
        if form.is_valid():
            pest.pest_name   = form.cleaned_data.get('pest_name')
            pest.pest_type   = form.cleaned_data.get('pest_type')
            pest.pest_url    = form.cleaned_data.get('pest_url')
            pest.description = form.cleaned_data.get('description')
            pest.management  = form.cleaned_data.get('management')
            # Process images - check for new image - if yes, delete any existing image
            if 'image_1' in request.FILES:
                if (pest.image_1):
                    pest.image_1.delete(save=False)
                pest.image_1   = request.FILES['image_1']
                pest.pest_thumbnail = request.FILES['image_1']
            pest.caption_1 = form.cleaned_data.get('caption_1')
            
            if 'image_2' in request.FILES:
                if (pest.image_2):
                    pest.image_2.delete(save=False)
                pest.image_2 = request.FILES['image_2']
            pest.caption_2 = form.cleaned_data.get('caption_2')

            if 'image_3' in request.FILES:
                if (pest.image_3):
                    pest.image_3.delete(save=False)
                pest.image_3 = request.FILES['image_3']
            pest.caption_3 = form.cleaned_data.get('caption_3') 

            if 'image_4' in request.FILES:
                if (pest.image_4):
                    pest.image_4.delete(save=False)
                pest.image_4 = request.FILES['image_4']
            pest.caption_4 = form.cleaned_data.get('caption_4')

            pest.save()

        response_data = {
            'status': 'success',
            'message': f'Received audio successfully',
        }
        return JsonResponse(response_data)
    else:
        form = PestAddUpdateForm(initial = { 'pest_name'   : pest.pest_name,
                                             'pest_type'   : pest.pest_type,
                                             'pest_url'    : pest.pest_url,
                                             'description' : pest.description,
                                             'management'  : pest.management,
                                             'image_1'     : pest.image_1,
                                             'caption_1'   : pest.caption_1,
                                             'image_2'     : pest.image_2,
                                             'caption_2'   : pest.caption_2,
                                             'image_3'     : pest.image_3,
                                             'caption_3'   : pest.caption_3,
                                             'image_4'     : pest.image_4,
                                             'caption_4'   : pest.caption_4,
                                           })
        context = { 'pest' : pest,
                    'form' : form }
        return render(request, 'pests/pest_edit.html', context)
  
def pest_delete(request, id):
    """ Delete selected pest from the Pest database table """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('plants:index'))
    pest = Pest.objects.get(id=id)
    if request.POST:
        pest.delete()
        return HttpResponseRedirect(reverse('pests:pest_summary')) 
    else:
        context = {'pest': pest}
        return render(request, 'pests/pest_delete_modal.html', context)
