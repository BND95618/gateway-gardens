# app/pests/admin.py

from django.contrib import admin

from django.contrib import admin
from pests.models   import Pest
    
class PestAdmin(admin.ModelAdmin):
    list_display = ("pest_name",
                    "pest_type",
                    "pest_url")

admin.site.register(Pest, PestAdmin)