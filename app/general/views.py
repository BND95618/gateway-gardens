# app/general/views.py
 
from django.contrib.auth.decorators import login_required, user_passes_test 
from django.shortcuts   import render

from core_utils.helpers import login_required_no_next, is_garden_editor

def index(request):
    """ Render the landing page for Gateway Gardens app """
    return render(request, 'general/index.html')

@login_required_no_next
def glossary(request):
    """ Render the Glossary Page for Gateway Gardens app """
    return render(request, 'general/glossary.html')

@login_required_no_next
def reference(request):
    """ Render the Reference Page for Gateway Gardens app """
    return render(request, 'general/reference.html')

@login_required_no_next
def about(request):
    """ Render the About Page for Gateway Gardens app """
    return render(request, 'general/about.html')

#

@login_required_no_next
@user_passes_test(is_garden_editor, login_url='general:index', redirect_field_name=None)
def fiddle(request):
    """ Render the Fiddle Page for testing of new functions """
    if request.method == 'POST':
        context = { 'fiddle' : 'fiddle', }
        return render(request, 'general/fiddle.html', context)
    else:
        context = { 'fiddle' : 'fiddle', }
        return render(request, 'general/fiddle.html', context)