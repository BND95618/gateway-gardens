from django.contrib import admin
from plants.models import Garden, MyPlant, Plant, Comment, Pest

# Register your models here.
class GardenAdmin(admin.ModelAdmin):
    list_display = ("name",
                    "owner",
                    "question",)
    prepopulated_fields = {"slug": ("name",) }
    
class MyPlantAdmin(admin.ModelAdmin):
    list_display = ("plant",
                    "owner",
                    "sun_exposure",)
    prepopulated_fields = {"slug": ("plant",) }
    
class PlantAdmin(admin.ModelAdmin):
    list_display = ("commonName", 
                    "genus", 
                    "species",)
    prepopulated_fields = {"slug": ("commonName",) }
  
class CommentAdmin(admin.ModelAdmin):
    list_display = ("author",
                    "subject",)
    prepopulated_fields = {"slug": ("author",) }

class PestAdmin(admin.ModelAdmin):
    list_display = ("pest_name",
                    "pest_type",
                    "pest_url")
  
admin.site.register(Garden,  GardenAdmin)
admin.site.register(MyPlant, MyPlantAdmin)
admin.site.register(Plant,   PlantAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Pest,     PestAdmin)