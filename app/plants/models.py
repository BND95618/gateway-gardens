# from uuid import uuid4 - youtube tutorial used this for image uniqueness (1:36:00)
from django.db import models

# app/plants/models.py

from django.conf import settings
from django.db   import models
from django.urls import reverse

from django_quill.fields import QuillField

class Garden(models.Model):
    """ My Garden description table """
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

class Plant(models.Model):
    """ Plant description table """
    commonName    = models.CharField(max_length=255)
    # Attributes
    type_x        = models.CharField(max_length=32,  default="tbd", blank=True)
    bloom_color   = models.CharField(max_length=128, default="tbd", blank=True)
    bloom_season  = models.CharField(max_length=64,  default="tbd", blank=True)
    height_feet   = models.IntegerField(default=0, blank=True, null=True)
    height_inch   = models.IntegerField(default=0, blank=True, null=True)
    width_feet    = models.IntegerField(default=0, blank=True, null=True)
    width_inch    = models.IntegerField(default=0, blank=True, null=True)
    sun_exposure  = models.CharField(max_length=128, default="tbd", blank=True)
    water_rqmts   = models.CharField(max_length=64,  default="tbd", blank=True)
    pH_min        = models.CharField(max_length=16,  default="tbd", blank=True)
    pH_max        = models.CharField(max_length=16,  default="tbd", blank=True)
    soil_type     = models.CharField(max_length=64,  default="tbd", blank=True)
    pollinators   = models.CharField(max_length=72,  default="tbd", blank=True)
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
    subkingdom    = models.CharField(max_length=64, default="tbd", blank=True)
    superdivision = models.CharField(max_length=64, default="tbd", blank=True)
    division      = models.CharField(max_length=64, default="tbd", blank=True)
    class_x       = models.CharField(max_length=64, default="tbd", blank=True)
    subclass      = models.CharField(max_length=64, default="tbd", blank=True)
    order         = models.CharField(max_length=64, default="tbd", blank=True)
    family        = models.CharField(max_length=64, default="tbd", blank=True)
    genus         = models.CharField(max_length=64, default="tbd", blank=True)
    species       = models.CharField(max_length=64, default="tbd", blank=True)
    variety       = models.CharField(max_length=64, default="tbd", blank=True)
    pronunciation = models.URLField(blank=True, null=True)
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
    creator_notes = QuillField(blank=True, null=True)
    plant_show    = models.CharField(max_length=8,  default="no", blank=True)
    plant_mine    = models.CharField(max_length=8,  default="no", blank=True)
    gardens       = models.ManyToManyField(Garden, blank=True)
    slug          = models.SlugField(default="", null=False)

    def __str__(self):
        return self.commonName
    
    def get_absolute_url(self):
        return reverse("plants_search")

class Comment(models.Model):
    """ Plant comments """
    # Many-to-one relationship - many "comments" can be associated with each "plant"
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
     
class MyPlant(models.Model):
    """ Plants that are in My Garden """
    # Many-to-one relationship - many "myplants" can be associated with each "plant"
    # connection to a specific plant in the Plant db table
    # related_name allows reverse look-up - find all 'myplants' that are associated with a particular 'plant'
    plant        = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='myplants')
    #
    owner        = models.CharField(max_length=64, default="tbd", blank=True)
    date         = models.DateField(auto_now_add=True)
    #
    date_planted = models.DateField(default="2000-01-01", null=True, blank=True)
 #   date_planted = models.DateField(blank=True)
    location     = models.CharField(max_length=64, default="tbd", blank=True)
    sun_exposure = models.CharField(max_length=64, default="tbd", blank=True)
    pH           = models.CharField(max_length=16, default="tbd", blank=True)
    soil_type    = models.CharField(max_length=64, default="tbd", blank=True)
    # Administrative stuff
    slug         = models.SlugField(default="tbd", null=False)

    def __str__(self):
        return self.location
    
    def get_absolute_url(self):
        return reverse("plants_search")

class MyPlantComment(models.Model):
    """ My Plant comments """
    # Many-to-one relationship 
    # - many "comments" can be associated with each "My Plant" record
    author  = models.CharField(max_length=64, default="tbd", blank=True)
    date    = models.DateField(auto_now_add=True)
    subject = models.CharField(max_length=64, default="tbd", blank=True)
    comment = QuillField(blank=True, null=True)
    # connection to a specific plant in the MyPlant db table
    myplant   = models.ForeignKey(MyPlant, on_delete=models.CASCADE)
    # Administrative stuff
    slug    = models.SlugField(default="", null=False)

    def __str__(self):
        return self.author
    
    def get_absolute_url(self):
        return reverse("myplants_details")