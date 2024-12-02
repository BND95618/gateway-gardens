# from uuid import uuid4 - youtube tutorial used this for image uniqueness (1:36:00)
from django.db import models

# app/plants/models.py

from django.conf import settings
from django.db   import models
from django.urls import reverse

from django_quill.fields import QuillField

# Garden description table
class Garden(models.Model):
    name         = models.CharField(max_length=64, default="tbd", blank=True)
    city         = models.CharField(max_length=32, default="tbd", blank=True)
    state        = models.CharField(max_length=16, default="tbd", blank=True)
    owner        = models.CharField(max_length=64, default="tbd", blank=True)
    usda_zone    = models.CharField(max_length=16, default="tbd", blank=True)
    sunset_zone  = models.CharField(max_length=32, default="tbd", blank=True)
    question     = models.CharField(max_length=8,  default="No",  blank=True)
    # Images
    image_1      = models.ImageField(upload_to='images/', blank=True, null=True)
    caption_1    = models.CharField(max_length=64, default="tbd", blank=True)
    image_2      = models.ImageField(upload_to='images/', blank=True, null=True)
    caption_2    = models.CharField(max_length=64, default="tbd", blank=True)
    image_3      = models.ImageField(upload_to='images/', blank=True, null=True)
    caption_3    = models.CharField(max_length=64, default="tbd", blank=True)
    image_4      = models.ImageField(upload_to='images/', blank=True, null=True)
    caption_4    = models.CharField(max_length=64, default="tbd", blank=True)
    image_5      = models.ImageField(upload_to='images/', blank=True, null=True)
    caption_5    = models.CharField(max_length=64, default="tbd", blank=True)
    image_6      = models.ImageField(upload_to='images/', blank=True, null=True)
    caption_6    = models.CharField(max_length=64, default="tbd", blank=True)
    image_7      = models.ImageField(upload_to='images/', blank=True, null=True)
    caption_7    = models.CharField(max_length=64, default="tbd", blank=True)
    image_8      = models.ImageField(upload_to='images/', blank=True, null=True)
    caption_8    = models.CharField(max_length=64, default="tbd", blank=True)
    # Administrative stuff
    slug         = models.SlugField(default="tbd", null=False)
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("plants_search")
    
# My Plants in My Garden - many-to-one relationship
class MyPlant(models.Model):
    # connection to a specific garden in the Garden db table
    plant        = models.ForeignKey(Garden, on_delete=models.CASCADE)
    #
    owner        = models.CharField(max_length=64, default="tbd", blank=True)
    date         = models.DateField(auto_now_add=True)
    location     = models.CharField(max_length=64, default="tbd", blank=True)
    sun_exposure = models.CharField(max_length=64, default="tbd", blank=True)
    # Administrative stuff
    slug         = models.SlugField(default="tbd", null=False)

    def __str__(self):
        return self.location
    
    def get_absolute_url(self):
        return reverse("plants_search")

# Plant description table
class Plant(models.Model):
    commonName    = models.CharField(max_length=255)
    # Attributes
    type_x        = models.CharField(max_length=32,  default="tbd", blank=True)
    bloom_color   = models.CharField(max_length=128, default="tbd", blank=True)
    bloom_season  = models.CharField(max_length=64,  default="tbd", blank=True)
    height_feet   = models.IntegerField(default=0, blank=True, null=True)
    height_inch   = models.IntegerField(default=0, blank=True, null=True)
    width_feet    = models.IntegerField(default=0, blank=True, null=True)
    width_inch    = models.IntegerField(default=0, blank=True, null=True)
    sun_exposure  = models.CharField(max_length=64,  default="tbd", blank=True)
    water_rqmts   = models.CharField(max_length=64,  default="tbd", blank=True)
    pH_min        = models.CharField(max_length=16,  default="tbd", blank=True)
    pH_max        = models.CharField(max_length=16,  default="tbd", blank=True)
    pollinators   = models.CharField(max_length=64,  default="tbd", blank=True)
    ucd_all_star  = models.CharField(max_length=8,   default="tbd", blank=True)
    ca_native     = models.CharField(max_length=8,   default="tbd", blank=True)
    usda_zone_min = models.CharField(max_length=32,  default="tbd", blank=True)
    usda_zone_max = models.CharField(max_length=32,  default="tbd", blank=True)
    sunset_zones  = models.CharField(max_length=32,  default="tbd", blank=True)
    # Text boxes
    description   = QuillField(blank=True, null=True)
    pruning       = QuillField(blank=True, null=True)
    fertilization = QuillField(blank=True, null=True)
    # Plant taxonomy
    kingdom       = models.CharField(max_length=64, default="tbd", blank=True)
    division      = models.CharField(max_length=64, default="tbd", blank=True)
    class_x       = models.CharField(max_length=64, default="tbd", blank=True)
    order         = models.CharField(max_length=64, default="tbd", blank=True)
    family        = models.CharField(max_length=64, default="tbd", blank=True)
    genus         = models.CharField(max_length=64, default="tbd", blank=True)
    species       = models.CharField(max_length=64, default="tbd", blank=True)
    variety       = models.CharField(max_length=64, default="tbd", blank=True)
    # Images
    image_1       = models.ImageField(upload_to='images/', blank=True, null=True)
    caption_1     = models.CharField(max_length=64, default="tbd", blank=True)
    image_2       = models.ImageField(upload_to='images/', blank=True, null=True)
    caption_2     = models.CharField(max_length=64, default="tbd", blank=True)
    image_3       = models.ImageField(upload_to='images/', blank=True, null=True)
    caption_3     = models.CharField(max_length=64, default="tbd", blank=True)
    image_4       = models.ImageField(upload_to='images/', blank=True, null=True)
    caption_4     = models.CharField(max_length=64, default="tbd", blank=True)
    # Administrative stuff
    creator       = models.CharField(max_length=64, default="tbd", blank=True)
    creation_date = models.DateField(auto_now_add=True)
    plant_show    = models.CharField(max_length=8,  default="No", blank=True)
    gardens       = models.ManyToManyField(Garden, blank=True)
    slug          = models.SlugField(default="", null=False)

    def __str__(self):
        return self.commonName
    
    def get_absolute_url(self):
        return reverse("plants_search")

# comments to plant many-to-one relationship
class Comment(models.Model):
    # db fields for the comment
    author  = models.CharField(max_length=64, default="tbd", blank=True)
    date    = models.DateField(auto_now_add=True)
    subject = models.CharField(max_length=64, default="tbd", blank=True)
    comment = QuillField(blank=True, null=True)
    # connection to a specific plant in the Plant db table
    plant   = models.ForeignKey(Plant, on_delete=models.CASCADE)
    # Administrative stuff
    slug    = models.SlugField(default="", null=False)

    def __str__(self):
        return self.author
    
    def get_absolute_url(self):
        return reverse("plants_search")
