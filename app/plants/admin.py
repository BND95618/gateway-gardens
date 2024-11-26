from django.contrib import admin
from plants.models import Plant, Comment, Garden

# Register your models here.
class GardenAdmin(admin.ModelAdmin):
    list_display = ("name",
                    "owner",
                    "question",)
    prepopulated_fields = {"slug": ("name",) }
    
class PlantAdmin(admin.ModelAdmin):
    list_display = ("commonName", 
                    "genus", 
                    "species",)
    prepopulated_fields = {"slug": ("commonName",) }
  
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author",
                    "subject",)
    prepopulated_fields = {"slug": ("author",) }
  
admin.site.register(Garden,  GardenAdmin)
admin.site.register(Plant,   PlantAdmin)
admin.site.register(Comment, CommentAdmin)