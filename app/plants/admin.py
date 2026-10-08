from django.contrib import admin
from plants.models  import Garden, MyPlant, MyPlantLog, MyPlantToDo, MyPlantComment, Plant, Comment
from pests.models   import Pest

# Register your models here.
class GardenAdmin(admin.ModelAdmin):
    list_display = ("owner",
                    "name",
                    "question",)
    prepopulated_fields = {"slug": ("name",) }
    
class MyPlantAdmin(admin.ModelAdmin):
    list_display = ("owner",
                    "plant",
                    "sun_exposure",)
    prepopulated_fields = {"slug": ("plant",) }

class MyPlantLogAdmin(admin.ModelAdmin):
    list_display = ("author",
                    "subject",)
    prepopulated_fields = {"slug": ("myplant",) }

class MyPlantToDoAdmin(admin.ModelAdmin):
    list_display = ("owner",
                    "complete",
                    "date",
                    "action",
                    "details",)
    prepopulated_fields = {"slug": ("myplant",) }

class MyPlantCommentAdmin(admin.ModelAdmin):
    list_display = ("author",
                    "date",
                    "subject",
                    "comment",)
    prepopulated_fields = {"slug": ("myplant",) }
    
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

class PestAdmin(admin.ModelAdmin):
    list_display = ("pest_name",
                    "pest_type",
                    "pest_url")
  
admin.site.register(Garden,         GardenAdmin)
admin.site.register(MyPlant,        MyPlantAdmin)
admin.site.register(MyPlantLog,     MyPlantLogAdmin)
admin.site.register(MyPlantToDo,    MyPlantToDoAdmin)
admin.site.register(MyPlantComment, MyPlantCommentAdmin)
admin.site.register(Plant,          PlantAdmin)
admin.site.register(Comment,        CommentAdmin)
admin.site.register(Pest,           PestAdmin)