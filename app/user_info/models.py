# /app/user_info/models.py

import os
import uuid  # Used to generate unique filenames for images

from django.db           import models
from django.conf         import settings
from django.urls         import reverse
from django.contrib.auth import get_user_model

# Process uploaded images to ensure reasonable sizes for storaging and rendering performance
from imagekit.models     import ProcessedImageField
from imagekit.processors import ResizeToFill
from imagekit.processors import Transpose # correct iPhone image rotation when directly using the camera

# Integrate Quill editor with Django project
from django_quill.fields import QuillField

# Store Django uploaded files as UUID files or inside UUID directories
from django_uuid_upload  import upload_to_uuid

#
def get_default_user():
    # Dynamically gets the active User model and returns a default ID
    User = get_user_model()
    # Returns the first user, or creates a system user if none exists
    user, created = User.objects.get_or_create(username='system_default')
    return user.pk

class UserInfo(models.Model):
    """ Auxiliary user information model """
    # User details (extends information in user database)
    profile_photo = ProcessedImageField(upload_to  = upload_to_uuid('images/'),
                                        processors = [Transpose(), ResizeToFill(800, 800)],
                                        format     = 'WEBP',
                                        options    = {'quality': 95},
                                        blank      = True, 
                                        null       = True)
    
    # Save the user's selection for plant search criteria
    common_name_search     = models.CharField(max_length=32, default="",    blank=True)
    genus_search           = models.CharField(max_length=32, default="",    blank=True)
    species_search         = models.CharField(max_length=32, default="",    blank=True)
    type_x_search          = models.CharField(max_length=32, default="Any", blank=True)
    bloom_color_search     = models.CharField(max_length=32, default="Any", blank=True)
    bloom_season_search    = models.CharField(max_length=32, default="Any", blank=True)
    bloom_month_search     = models.CharField(max_length=32, default="Any", blank=True)
    pollinators_search     = models.CharField(max_length=32, default="Any", blank=True)
    ca_native_search       = models.CharField(max_length=32, default="Any", blank=True)
    ucd_all_star_search    = models.CharField(max_length=32, default="Any", blank=True)
    davis_trees_search     = models.CharField(max_length=32, default="Any", blank=True)
    sunset_z14_search      = models.CharField(max_length=32, default="Any", blank=True)
    sun_exposure_search    = models.CharField(max_length=32, default="Any", blank=True)
    water_rqmts_search     = models.CharField(max_length=32, default="Any", blank=True)
    pH_search              = models.CharField(max_length=32, default="Any", blank=True)
    soil_type_search       = models.CharField(max_length=32, default="Any", blank=True)
    heat_tolerance_search  = models.CharField(max_length=32, default="Any", blank=True)
    deer_resistance_search = models.CharField(max_length=32, default="Any", blank=True)
    usda_zone_search       = models.CharField(max_length=32, default="Any", blank=True)
    sunset_zone_search     = models.CharField(max_length=32, default="Any", blank=True)
    garden_search          = models.CharField(max_length=32, default="Any", blank=True)

    # Admin
    status_search          = models.CharField(max_length=16, default="Any", blank=True)

    # Save the user's selection for my plant search criteria
    my_sun_exposure_search = models.CharField(max_length=32, default="Any", blank=True)
    my_water_level_search  = models.CharField(max_length=32, default="Any", blank=True)
    my_soil_type_search    = models.CharField(max_length=32, default="Any", blank=True)
    my_happiness_search    = models.CharField(max_length=32, default="Any", blank=True)

    # Save the user's selection for the my plants column chooser
    my_column_selection = models.CharField(max_length=256,  blank=True,
                          default=["Common Name", "Genus/Species", "Variety", "Type", 
                                   "Location", "Sun Exposure", "pH", "Happy?"],)
    
    # Save the user's selection for the all plants column chooser
    column_selection    = models.CharField(max_length=256,  blank=True,
                          default=["Common Name", "Type", "Height", "Width", 
                                   "Bloom Color", "Bloom Season", "Pollinators"],)
    
    # Save the user's most recent To Do table sort column and direction
    lastToDoSortCol = models.IntegerField(default=1, blank=True, null=True)
    lastToDoSortDir = models.CharField(max_length=8, default="up", blank=True)

    # JSON array of shapes for garden design
    shapes_JSON = models.JSONField(default=list, blank=True)

    # Connection to a specific user in the User db table
    # If the user is deleted, delete their assiciated garden
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, default=get_default_user)

    # AR: Implement slug field
    slug = models.SlugField(default="tbd", null=False, blank=True)
        
    def __str__(self):
        return self.common_name_search
    
    def get_absolute_url(self):
        return reverse("plants_summary")
