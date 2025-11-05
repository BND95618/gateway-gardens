# app/plants/models.py

from django.db   import models
from django.conf import settings
from django.urls import reverse

from django_quill.fields import QuillField

# from uuid import uuid4 - youtube tutorial used this for image uniqueness (1:36:00)

class Garden(models.Model):
    """ My Garden description table - linked to one particular user """
    name          = models.CharField(max_length=64, default="tbd", blank=True, null=True)
    city          = models.CharField(max_length=32, default="tbd", blank=True, null=True)
    state         = models.CharField(max_length=16, default="tbd", blank=True, null=True)
    owner         = models.CharField(max_length=64, default="tbd", blank=True, null=True)
    usda_zone     = models.CharField(max_length=16, default="tbd", blank=True, null=True)
    sunset_zone   = models.CharField(max_length=32, default="tbd", blank=True, null=True)
    question      = models.CharField(max_length=8,  default="No",  blank=True, null=True)
    # Images
    image_1       = models.ImageField(upload_to='images/', blank=True, null=True)
    caption_1     = models.CharField(max_length=64, default="tbd", blank=True)
    image_2       = models.ImageField(upload_to='images/', blank=True, null=True)
    caption_2     = models.CharField(max_length=64, default="tbd", blank=True)
    image_3       = models.ImageField(upload_to='images/', blank=True, null=True)
    caption_3     = models.CharField(max_length=64, default="tbd", blank=True)
    image_4       = models.ImageField(upload_to='images/', blank=True, null=True)
    caption_4     = models.CharField(max_length=64, default="tbd", blank=True)
    image_5       = models.ImageField(upload_to='images/', blank=True, null=True)
    caption_5     = models.CharField(max_length=64, default="tbd", blank=True)
    image_6       = models.ImageField(upload_to='images/', blank=True, null=True)
    caption_6     = models.CharField(max_length=64, default="tbd", blank=True)
    image_7       = models.ImageField(upload_to='images/', blank=True, null=True)
    caption_7     = models.CharField(max_length=64, default="tbd", blank=True)
    image_8       = models.ImageField(upload_to='images/', blank=True, null=True)
    caption_8     = models.CharField(max_length=64, default="tbd", blank=True)
    # Administrative stuff
    # Save the user's selection for plant search criteria
    type_x_search       = models.CharField(max_length=32, default="Any", blank=True)
    bloom_color_search  = models.CharField(max_length=32, default="Any", blank=True)
    bloom_season_search = models.CharField(max_length=32, default="Any", blank=True)
    bloom_month_search  = models.CharField(max_length=32, default="Any", blank=True)
    pollinators_search  = models.CharField(max_length=32, default="Any", blank=True)
    ca_native_search    = models.CharField(max_length=32, default="Any", blank=True)
    ucd_all_star_search = models.CharField(max_length=32, default="Any", blank=True)
    sun_exposure_search = models.CharField(max_length=32, default="Any", blank=True)
    water_rqmts_search  = models.CharField(max_length=32, default="Any", blank=True)
    pH_search           = models.CharField(max_length=32, default="Any", blank=True)
    soil_type_search    = models.CharField(max_length=32, default="Any", blank=True)
    usda_zone_search    = models.CharField(max_length=32, default="Any", blank=True)
    sunset_zone_search  = models.CharField(max_length=32, default="Any", blank=True)
    garden_search       = models.CharField(max_length=32, default="Any", blank=True)
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
    # AR: Implement slug field
    slug                = models.SlugField(default="tbd", null=False, blank=True)
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("plants_summary")

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
    bloom_season      = models.CharField(max_length=64,  default="tbd", blank=True)
    bloom_start       = models.CharField(max_length=8,   default="tbd", blank=True)
    bloom_end         = models.CharField(max_length=8,   default="tbd", blank=True)
    bloom_months      = models.CharField(max_length=128, default="tbd", blank=True)
    pollinators       = models.CharField(max_length=72,  default="tbd", blank=True)
    ca_native         = models.CharField(max_length=8,   default="tbd", blank=True)
    ucd_all_star      = models.CharField(max_length=8,   default="tbd", blank=True)
    sun_exposure      = models.CharField(max_length=128, default="tbd", blank=True)
    water_rqmts       = models.CharField(max_length=64,  default="tbd", blank=True)
    pH_min            = models.CharField(max_length=16,  default="tbd", blank=True)
    pH_max            = models.CharField(max_length=16,  default="tbd", blank=True)
    soil_type         = models.CharField(max_length=64,  default="tbd", blank=True)
    usda_zone_min     = models.CharField(max_length=32,  default="tbd", blank=True)
    usda_zone_max     = models.CharField(max_length=32,  default="tbd", blank=True)
    sunset_zones      = models.CharField(max_length=32,  default="tbd", blank=True)
    # Text boxes
    description       = QuillField(blank=True, null=True)
    pruning           = QuillField(blank=True, null=True)
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
    variety           = models.CharField(max_length=64, default="tbd", blank=True)
    phonetic_spelling = models.CharField(max_length=32, default="tbd", blank=True)
    audio_name        = models.FileField(upload_to='audio/', blank=True, null=True)
    # Images
    image_1           = models.ImageField(upload_to='images/', blank=True, null=True)
    caption_1         = models.CharField(max_length=64, default="tbd", blank=True)
    image_2           = models.ImageField(upload_to='images/', blank=True, null=True)
    caption_2         = models.CharField(max_length=64, default="tbd", blank=True)
    image_3           = models.ImageField(upload_to='images/', blank=True, null=True)
    caption_3         = models.CharField(max_length=64, default="tbd", blank=True)
    image_4           = models.ImageField(upload_to='images/', blank=True, null=True)
    caption_4         = models.CharField(max_length=64, default="tbd", blank=True)
    # Administrative stuff
    creator           = models.CharField(max_length=64, default="tbd", blank=True)
    creation_date     = models.DateField(auto_now_add=True)
    creator_notes     = QuillField(blank=True, null=True)
    # Tags a plant for display/hidden in a summary table
    plant_show        = models.CharField(max_length=8,  default="no", blank=True)
    # Indicates if a user has indicated that a particular plant is in their garden
    # during the plant filtering process
    plant_mine        = models.CharField(max_length=8,  default="no", blank=True)
    gardens           = models.ManyToManyField(Garden, related_name="plants")
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
    # connection to a specific plant in the Plant db table
    plant   = models.ForeignKey(Plant, on_delete=models.CASCADE)
    # Administrative stuff
    slug    = models.SlugField(default="", null=False, blank=True)

    def __str__(self):
        return self.author
    
    def get_absolute_url(self):
        return reverse("plants_summary")
     
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
    # Tags a plant for display/hidden in a summary table
    show         = models.CharField(max_length=8,   default="no", blank=True)
    # Save the user's most recent To Do table sort column and direction
    lastToDoSortCol = models.IntegerField(default=1, blank=True, null=True)
    lastToDoSortDir = models.CharField(max_length=8, default="up", blank=True)
    # Administrative stuff
    slug         = models.SlugField(default="tbd", null=False, blank=True)

    def __str__(self):
        return self.location
    
    def get_absolute_url(self):
        return reverse("plants_summary")

class MyPlantToDo(models.Model):
    """ My Plant To Do """
    # Many-to-one relationship 
    owner    = models.CharField(max_length=64, default="tbd", blank=True)
    # - many "To Do items" can be associated with each "My Plant" record
    complete = models.BooleanField(default=False)
    date     = models.DateField(default="2025-01-01", null=True, blank=True)
    action   = models.CharField(max_length=16, default="", blank=True)
    details  = models.CharField(max_length=64, default="", blank=True)
    repeat   = models.CharField(max_length=16, default="", blank=True)
    # connection to a specific plant in the MyPlant db table
    myplant   = models.ForeignKey(MyPlant, on_delete=models.CASCADE)
    # Administrative stuff
    slug    = models.SlugField(default="", null=False, blank=True)

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
    # connection to a specific plant in the MyPlant db table
    myplant   = models.ForeignKey(MyPlant, on_delete=models.CASCADE)
    # Administrative stuff
    slug    = models.SlugField(default="", null=False, blank=True)

    def __str__(self):
        return self.author
    
    def get_absolute_url(self):
        return reverse("myplant_details")

class Pest(models.Model):
    pest_name = models.CharField(max_length=32)
    pest_type = models.CharField(max_length=32,  default="tbd", blank=True)
    pest_url  = models.URLField(default="tbd", blank=True)
    # Many-to-Many relationship - many different "pests" can be associated with many different "Plant" records
    plants    = models.ManyToManyField(Plant)

    def __str__(self):
        return self.pest_name
    
    def get_absolute_url(self):
        return reverse("plants_summary")

# class Fiddle(models.Model):