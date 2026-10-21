# app/plants/models.py

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

class Plant(models.Model):
    """ Plant description table """
    commonName        = models.CharField(max_length=255)
    # Attributes
    type_x            = models.CharField(max_length=32,  default="tbd", blank=True)
    height_feet       = models.IntegerField(default=0,   blank=True, null=True)
    height_inch       = models.IntegerField(default=0,   blank=True, null=True)
    width_feet        = models.IntegerField(default=0,   blank=True, null=True)
    width_inch        = models.IntegerField(default=0,   blank=True, null=True)
    bloom_color       = models.CharField(max_length=128, default="tbd", blank=True)
    bloom_season      = models.CharField(max_length=128, default="tbd", blank=True)
    bloom_start       = models.CharField(max_length=8,   default="tbd", blank=True)
    bloom_end         = models.CharField(max_length=8,   default="tbd", blank=True)
    bloom_months      = models.CharField(max_length=128, default="tbd", blank=True)
    pollinators       = models.CharField(max_length=72,  default="tbd", blank=True)
    ca_native         = models.CharField(max_length=8,   default="tbd", blank=True)
    ucd_all_star      = models.CharField(max_length=8,   default="No",  blank=True)
    davis_trees       = models.CharField(max_length=8,   default="No",  blank=True)
    sunset_z14        = models.CharField(max_length=8,   default="tbd", blank=True)
    sun_exposure      = models.CharField(max_length=128, default="tbd", blank=True)
    water_rqmts       = models.CharField(max_length=64,  default="tbd", blank=True)
    pH_min            = models.CharField(max_length=16,  default="tbd", blank=True)
    pH_max            = models.CharField(max_length=16,  default="tbd", blank=True)
    soil_type         = models.CharField(max_length=64,  default="tbd", blank=True)
    heat_tolerance    = models.CharField(max_length=32,  default="tbd", blank=True) 
    deer_resistance   = models.CharField(max_length=32,  default="tbd", blank=True) 
    usda_zone_min     = models.CharField(max_length=32,  default="tbd", blank=True)
    usda_zone_max     = models.CharField(max_length=32,  default="tbd", blank=True)
    sunset_zones      = models.CharField(max_length=32,  default="tbd", blank=True)
    # Text boxes
    description       = QuillField(blank=True, null=True)
    pruning           = QuillField(blank=True, null=True)
    pruning_video     = models.URLField(default="", blank=True)
    fertilization     = QuillField(blank=True, null=True)
    propagation       = QuillField(blank=True, null=True)
    pests_diseases    = QuillField(blank=True, null=True)
    # Plant taxonomy
    kingdom           = models.CharField(max_length=64, default="tbd", blank=True)
    subkingdom        = models.CharField(max_length=64, default="tbd", blank=True)
    superdivision     = models.CharField(max_length=64, default="tbd", blank=True)
    division          = models.CharField(max_length=64, default="tbd", blank=True)
    class_x           = models.CharField(max_length=64, default="tbd", blank=True)
    subclass          = models.CharField(max_length=64, default="tbd", blank=True)
    order             = models.CharField(max_length=64, default="tbd", blank=True)
    family            = models.CharField(max_length=64, default="tbd", blank=True)
    genus             = models.CharField(max_length=64, default="tbd", blank=True)
    species           = models.CharField(max_length=64, default="tbd", blank=True)
    subspecies        = models.CharField(max_length=64, default="tbd", blank=True)
    variety           = models.CharField(max_length=64, default="tbd", blank=True)
    cultivar          = models.CharField(max_length=64, default="tbd", blank=True)
    phonetic_spelling = models.CharField(max_length=64, default="tbd", blank=True)
    # Scientific name pronunciation audio
    audio_name        = models.FileField(upload_to     = upload_to_uuid('audio/'),
                                         blank         = True, 
                                         null          = True)
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
    # Administrative stuff
    creator           = models.CharField(max_length=64, default="tbd", blank=True)
    creation_date     = models.DateField(auto_now_add=True)
    creator_notes     = QuillField(blank=True, null=True)
    status            = models.CharField(max_length=16, default="Development", blank=True)
    # Tags a plant for display/hidden in a summary table
    plant_show        = models.CharField(max_length=8,  default="no", blank=True)
    # Indicates if a user has indicated that a particular plant is in their garden
    # during the plant filtering process
    plant_mine        = models.CharField(max_length=16,  default="no", blank=True)
    #
    gardens           = models.ManyToManyField('mygarden.Garden', related_name="plants", blank=True)
    # 
    slug              = models.SlugField(default="", null=False, blank=True)

    def __str__(self):
        return self.commonName
    
    def get_absolute_url(self):
        return reverse("plants_summary")

class Comment(models.Model):
    """ Plant comments """
    # Many-to-one relationship - many "comments" can be associated with each "plant"
    # db fields for the comment
    author  = models.CharField(max_length=64, default="tbd", blank=True)
    date    = models.DateField(auto_now_add=True)
    subject = models.CharField(max_length=64, default="tbd", blank=True)
    comment = QuillField(blank=True, null=True)
    # Many-to-one relationship 
    # - connection to a specific plant in the Plant db table
    # - many "Comments" can be associated with each "Plant" record
    # - if the associated plant is deleted then the comment is automatically deleted
    plant   = models.ForeignKey(Plant, on_delete=models.CASCADE)
    # Administrative stuff
    slug    = models.SlugField(default="", null=False, blank=True)

    def __str__(self):
        return self.author
    
    def get_absolute_url(self):
        return reverse("plants_summary")