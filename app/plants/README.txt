app > plants > README
##################################################################################
Local build and deployment
##################################################################################
# Open Docker Desktop application

# Create image:

  % docker build -t plants-local .

# Spin up the container

  % docker-compose up

# Create image and run image locally

  http://127.0.0.1:8000/

# To stop the container

  ^C

# To take down the container

  % docker-compose down
----------------------------------------------------------------------------------
# Update database (only if model changes were made):

  % docker-compose exec app python manage.py makemigrations plants
  % docker-compose exec app python manage.py migrate

# Collect static files (only if changes were made to static files):

  % docker-compose exec app python manage.py collectstatic

# Rebuild image after requirements.txt update

  > Delete running container
  > Delete existing images
  % docker-compose up

# Check which requirements have been installed

  % docker-compose exec app pip list

# Create a new superuser

  % docker-compose exec app python manage.py createsuperuser

# After new db creation

  1. Create superuser account
  2. Login into admin account as superuser
  3. Create groups
      - Gardener 
      - Garden-Contributor
      - Garden-Editor
##################################################################################
AWS Lightsail build and deployment
##################################################################################
# Create image:

  % docker build -t plants --platform linux/x86_64 .

# Authenticate via AWS CLI

# Push image to AWS Lightsail

  % aws lightsail push-container-image --service-name plants --label v1 --image plants:latest 

# Running migrations - launch command (deployment will fail and will need to be 
# rerun w/o the launch command)

  % python manage.py migrate --noinput

# Go to AWS Lightsail and change to new image

  > Log in
    - AWS account #: ************
  > Click "Save and Deploy"
  > Click on new link
##################################################################################
User Groups:
##################################################################################
> Gardener
> Garden-Conributor
> Garden-Editor
##################################################################################
Django response objects
##################################################################################
Every view function is responsible for returning an HttpResponse object. This 
object contains the content and metadata that will be sent back to the client's 
web browser.

  template = loader.get_template("plants/gardens_summary.html")
  return HttpResponse(template.render(context, request))

'return render' is a common shortcut function used in views to combine a given 
template with a context dictionary and return an HttpResponse object containing 
the rendered HTML.

  return render(request, 'plants/plant_edit.html', context)

'HttpResponseRedirect' is a class within django.http that facilitates redirecting
a user's browser to a different URL. It is commonly used after processing form
data (especially POST requests) to prevent resubmission if the user refreshes
the page, a practice known as the "Post/Redirect/Get" pattern.

  return HttpResponseRedirect(reverse('plants:myplants_summary'))

To return a JSON response in Django, the primary method involves using the 
JsonResponse class from django.http

  return JsonResponse({'shapes_JSON' : shapes_JSON})

##################################################################################
Cheatsheet: Docker
##################################################################################
#  Check to see what versions are running:

  % docker --version
  % docker compose version

# List running containers:

  % docker ps

# List of local images:

  % docker images

# Confirm that Docker was successfully installed

  %  docker run hello-world

# Bring up  the container 

  % docker-compose up - --build

# Shut down the container 

  % docker-compose down

# Read console log

  % docker logs <container>
##################################################################################