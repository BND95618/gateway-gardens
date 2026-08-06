# app/pests/models.py

import os
import uuid  # Used to generate unique filenames for images

from django.db           import models
from django.conf         import settings
from django.urls         import reverse

# Process uploaded images to ensure reasonable sizes for storaging and rendering performance
from imagekit.models     import ProcessedImageField
from imagekit.processors import ResizeToFill
from imagekit.processors import Transpose # correct iPhone image rotation when directly using the camera

# Integrate Quill editor with Django project
from django_quill.fields import QuillField

# Store Django uploaded files as UUID files or inside UUID directories
from django_uuid_upload  import upload_to_uuid

class Pest(models.Model):
    pest_name   = models.CharField(max_length=32)
    pest_type   = models.CharField(max_length=32,  default="tbd", blank=True)
    pest_url    = models.URLField(default="tbd", blank=True)
    description = QuillField(blank=True, null=True)
    management  = QuillField(blank=True, null=True)

    image_1   = ProcessedImageField(upload_to  = upload_to_uuid('images/'),
                    processors = [Transpose(), ResizeToFill(800, 800)],
                    format     = 'WEBP',
                    options    = {'quality': 95},
                    blank      = True, 
                    null       = True)
    caption_1 = models.CharField(max_length=64, default="tbd", blank=True)

    image_2   = ProcessedImageField(upload_to = upload_to_uuid('images/'),
                processors = [Transpose(), ResizeToFill(800, 800)],
                format     = 'WEBP',
                options    = {'quality': 95},
                blank      = True, 
                null       = True)
    caption_2 = models.CharField(max_length=64, default="tbd", blank=True)

    image_3   = ProcessedImageField(upload_to = upload_to_uuid('images/'),
                processors = [Transpose(), ResizeToFill(800, 800)],
                format     = 'WEBP',
                options    = {'quality': 95},
                blank      = True, 
                null       = True)
    caption_3 = models.CharField(max_length=64, default="tbd", blank=True)

    image_4   = ProcessedImageField(upload_to = upload_to_uuid('images/'),
                processors = [Transpose(), ResizeToFill(800, 800)],
                format     = 'WEBP',
                options    = {'quality': 95},
                blank      = True, 
                null       = True)
    caption_4 = models.CharField(max_length=64, default="tbd", blank=True)

    pest_thumbnail = ProcessedImageField(upload_to = upload_to_uuid('images/'),
                     processors = [Transpose(), ResizeToFill(150, 150)],
                     format     = 'WEBP',
                     options    = {'quality': 95},
                     blank      = True, 
                     null       = True)
    
    # Many-to-Many relationship - many different "pests" can be associated with many different "Plant" records
    plants    = models.ManyToManyField('plants.Plant')

    def __str__(self):
        return self.pest_name
    
    def get_absolute_url(self):
        return reverse("plants_summary")