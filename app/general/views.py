# app/plants/views.py
 
from django.http      import HttpResponse, HttpResponseRedirect, JsonResponse 
from django.shortcuts import render, redirect # Added for images
from django.template  import loader
from django.urls      import reverse

def index(request):
    """ Render the landing page for Gateway Gardens app """
    return render(request, 'general/index.html')

def glossary(request):
    """ Render the Glossary Page for Gateway Gardens app """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    return render(request, 'general/glossary.html')

def reference(request):
    """ Render the Reference Page for Gateway Gardens app """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    return render(request, 'general/reference.html')

def about(request):
    """ Render the About Page for Gateway Gardens app """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    return render(request, 'general/about.html')

#

def fiddle(request):
    """ Render the Fiddle Page for testing of new functions """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    if request.method == 'POST':
        context = { 'fiddle' : 'fiddle', }
        return render(request, 'general/fiddle.html', context)
    else:
        context = { 'fiddle' : 'fiddle', }
        return render(request, 'general/fiddle.html', context)

def debug(request):
    """ Render the Debug Page for debugging of new functions """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('general:index'))
    return render(request, 'plants/debug.html')