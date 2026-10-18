# /app/mygarden/admin.py

from django.contrib import admin
from mygarden.models  import Garden

class GardenAdmin(admin.ModelAdmin):
    list_display = ("owner",
                    "name",
                    "question",)
    prepopulated_fields = {"slug": ("name",) }
  
admin.site.register(Garden, GardenAdmin)