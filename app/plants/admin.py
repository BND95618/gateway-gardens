# /app/plants/admin.py

from django.contrib import admin
from plants.models  import Plant, Comment
   
class PlantAdmin(admin.ModelAdmin):
    list_display = ("creator",
                    "commonName", 
                    "genus", 
                    "species",)
    prepopulated_fields = {"slug": ("commonName",) }
  
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author",
                    "subject",)
    prepopulated_fields = {"slug": ("author",) }

admin.site.register(Plant,          PlantAdmin)
admin.site.register(Comment,        CommentAdmin)