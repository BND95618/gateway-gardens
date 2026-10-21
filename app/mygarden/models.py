# /app/mygarden/models.py

from django.db           import models
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

class Garden(models.Model):
    """ My Garden description table - linked to one particular user """
    # User garden details
    name          = models.CharField(max_length=64, default="tbd", blank=True, null=True)
    city          = models.CharField(max_length=32, default="tbd", blank=True, null=True)
    state         = models.CharField(max_length=16, default="tbd", blank=True, null=True)
    owner         = models.CharField(max_length=64, default="tbd", blank=True, null=True)
    usda_zone     = models.CharField(max_length=16, default="tbd", blank=True, null=True)
    sunset_zone   = models.CharField(max_length=32, default="tbd", blank=True, null=True)
    description   = QuillField(blank=True, null=True)
    question      = models.CharField(max_length=8,  default="No",  blank=True, null=True)
    # Images
    image_1       = ProcessedImageField(upload_to  = upload_to_uuid('images/'),
                                        processors = [Transpose(), ResizeToFill(800, 600)],
                                        format     = 'WEBP',
                                        options    = {'quality': 95},
                                        blank      = True, 
                                        null       = True)
    caption_1     = models.CharField(max_length=64, default="tbd", blank=True)

    image_2       = ProcessedImageField(upload_to  = upload_to_uuid('images/'),
                                        processors = [Transpose(), ResizeToFill(800, 600)],
                                        format     = 'WEBP',
                                        options    = {'quality': 95},
                                        blank      = True, 
                                        null       = True)
    caption_2     = models.CharField(max_length=64, default="tbd", blank=True)

    image_3       = ProcessedImageField(upload_to  = upload_to_uuid('images/'),
                                        processors = [Transpose(), ResizeToFill(800, 600)],
                                        format     = 'WEBP',
                                        options    = {'quality': 95},
                                        blank      = True, 
                                        null       = True)
    caption_3     = models.CharField(max_length=64, default="tbd", blank=True)

    image_4       = ProcessedImageField(upload_to  = upload_to_uuid('images/'),
                                        processors = [Transpose(), ResizeToFill(800, 600)],
                                        format     = 'WEBP',
                                        options    = {'quality': 95},
                                        blank      = True, 
                                        null       = True)
    caption_4     = models.CharField(max_length=64, default="tbd", blank=True)

    image_5       = ProcessedImageField(upload_to  = upload_to_uuid('images/'),
                                        processors = [Transpose(), ResizeToFill(800, 600)],
                                        format     = 'WEBP',
                                        options    = {'quality': 95},
                                        blank      = True, 
                                        null       = True)
    caption_5     = models.CharField(max_length=64, default="tbd", blank=True)

    image_6       = ProcessedImageField(upload_to  = upload_to_uuid('images/'),
                                        processors = [Transpose(), ResizeToFill(800, 600)],
                                        format     = 'WEBP',
                                        options    = {'quality': 95},
                                        blank      = True, 
                                        null       = True)
    caption_6     = models.CharField(max_length=64, default="tbd", blank=True)

    image_7       = ProcessedImageField(upload_to  = upload_to_uuid('images/'),
                                        processors = [Transpose(), ResizeToFill(800, 600)],
                                        format     = 'WEBP',
                                        options    = {'quality': 95},
                                        blank      = True, 
                                        null       = True)
    caption_7     = models.CharField(max_length=64, default="tbd", blank=True)

    image_8       = ProcessedImageField(upload_to  = upload_to_uuid('images/'),
                                        processors = [Transpose(), ResizeToFill(800, 600)],
                                        format     = 'WEBP',
                                        options    = {'quality': 95},
                                        blank      = True, 
                                        null       = True)
    caption_8     = models.CharField(max_length=64, default="tbd", blank=True)
    
    # AR: Implement slug field
    slug          = models.SlugField(default="tbd", null=False, blank=True)
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("plants_summary")
