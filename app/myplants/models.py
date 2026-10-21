# /app/myplants/models.py

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
class MyPlant(models.Model):
    """ Plants that are in My Garden """
    # Many-to-one relationship 
    # - connection to a specific plant in the Plant db table
    # - many "My Plant" items can be associated with each "Plant" record
    # - if the associated plant is deleted then the "My Plant" item is automatically deleted
    plant        = models.ForeignKey('plants.Plant', on_delete=models.CASCADE, related_name='myplants')
    #
    owner        = models.CharField(max_length=64, default="tbd", blank=True)
    date         = models.DateField(auto_now_add=True)
    #
    date_planted = models.DateField(default="2000-01-01", null=True, blank=True)
    bloom_color  = models.CharField(max_length=32,  default="tbd", blank=True)
    bloom_start  = models.CharField(max_length=8,   default="tbd", blank=True)
    bloom_end    = models.CharField(max_length=8,   default="tbd", blank=True)
    bloom_months = models.CharField(max_length=128, default="tbd", blank=True)
    location     = models.CharField(max_length=64,  default="tbd", blank=True)
    sun_exposure = models.CharField(max_length=64,  default="tbd", blank=True)
    water_level  = models.CharField(max_length=64,  default="tbd", blank=True)
    soil_type    = models.CharField(max_length=64,  default="tbd", blank=True)
    pH           = models.CharField(max_length=16,  default="tbd", blank=True)
    happiness    = models.CharField(max_length=32,  default="tbd", blank=True)
    notes        = QuillField(blank=True, null=True)
    status       = models.CharField(max_length=16,  default="not_in_my_garden", blank=True)
    # Tags a plant for display/hidden in a summary table
    show         = models.CharField(max_length=8,   default="no", blank=True)
    # Administrative stuff
    slug         = models.SlugField(default="tbd", null=False, blank=True)

    def __str__(self):
        return self.location
    
    def get_absolute_url(self):
        return reverse("plants_summary")

class MyPlantLog(models.Model):
    """ My Plant Log Entries """
    # Many-to-one relationship 
    # - many "log entries" can be associated with each "My Plant" record
    author  = models.CharField(max_length=64, default="tbd", blank=True)
    subject = models.CharField(max_length=64, default="tbd", blank=True)
    date    = models.DateField(auto_now_add=True)
    entry   = QuillField(blank=True, null=True)
    # Images
    image_1   = ProcessedImageField(upload_to  = upload_to_uuid('images/'),
                    processors = [Transpose(), ResizeToFill(800, 800)],
                    format     = 'WEBP',
                    options    = {'quality': 95},
                    blank      = True, 
                    null       = True)
    caption_1 = models.CharField(max_length=64, default="tbd", blank=True)
    image_2   = ProcessedImageField(upload_to  = upload_to_uuid('images/'),
                    processors = [Transpose(), ResizeToFill(800, 800)],
                    format     = 'WEBP',
                    options    = {'quality': 95},
                    blank      = True, 
                    null       = True)
    caption_2 = models.CharField(max_length=64, default="tbd", blank=True)
    image_3   = ProcessedImageField(upload_to  = upload_to_uuid('images/'),
                    processors = [Transpose(), ResizeToFill(800, 800)],
                    format     = 'WEBP',
                    options    = {'quality': 95},
                    blank      = True, 
                    null       = True)
    caption_3 = models.CharField(max_length=64, default="tbd", blank=True)
    image_4   = ProcessedImageField(upload_to  = upload_to_uuid('images/'),
                    processors = [Transpose(), ResizeToFill(800, 800)],
                    format     = 'WEBP',
                    options    = {'quality': 95},
                    blank      = True, 
                    null       = True)
    caption_4 = models.CharField(max_length=64, default="tbd", blank=True)
    # Many-to-one relationship 
    # - connection to a specific plant in the MyPlant db table
    # - many "Log Entries" items can be associated with each "My Plant" record
    # - if the associated myplant is deleted then the "Log Entries" item is automatically deleted
    myplant   = models.ForeignKey('myplants.MyPlant', on_delete=models.CASCADE, related_name='myplantlogs')
    # Administrative stuff
    slug    = models.SlugField(default="", null=False, blank=True)

    def __str__(self):
        return self.author
    
    def get_absolute_url(self):
        return reverse("myplant_details")

class MyPlantToDo(models.Model):
    """ My Plant To Do """
    owner      = models.CharField(max_length=64, default="tbd", blank=True)
    
    commonName = models.CharField(max_length= 32, default="", blank=True)
    pruning    = QuillField(blank=True, null=True)

    complete   = models.BooleanField(default=False)
    date       = models.DateField(default="2025-01-01", null=True, blank=True)
    action     = models.CharField(max_length= 16, default="", blank=True)
    details    = models.CharField(max_length=256, default="", blank=True)
    repeat     = models.CharField(max_length= 16, default="", blank=True)
    # Many-to-one relationship 
    # - connection to a specific plant in the MyPlant db table
    # - many "To Do" items can be associated with each "My Plant" record
    # - if the associated myplant is deleted then the "To Do" item is automatically deleted
    myplant    = models.ForeignKey('myplants.MyPlant', on_delete=models.CASCADE, related_name='myplanttodos')
    # Administrative stuff
    slug       = models.SlugField(default="", null=False, blank=True)

    def __str__(self):
        return self.action
    
    def get_absolute_url(self):
        return reverse("myplant_details")

class MyPlantComment(models.Model):
    """ My Plant comments """
    # Many-to-one relationship 
    # - many "comments" can be associated with each "My Plant" record
    author  = models.CharField(max_length=64, default="tbd", blank=True)
    date    = models.DateField(auto_now_add=True)
    subject = models.CharField(max_length=64, default="tbd", blank=True)
    comment = QuillField(blank=True, null=True)
    # Many-to-one relationship 
    # - connection to a specific plant in the MyPlant db table
    # - many "Comments" can be associated with each "My Plant" record
    # - if the associated myplant is deleted then the comment is automatically deleted
    myplant   = models.ForeignKey('myplants.MyPlant', on_delete=models.CASCADE, related_name='myplantcomments')
    # Administrative stuff
    slug    = models.SlugField(default="", null=False, blank=True)

    def __str__(self):
        return self.author
    
    def get_absolute_url(self):
        return reverse("myplant_details")
 