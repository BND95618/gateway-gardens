# /app/myplants/admin.py

from django.contrib  import admin
from myplants.models import MyPlant, MyPlantLog, MyPlantToDo, MyPlantComment

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

admin.site.register(MyPlant,        MyPlantAdmin)
admin.site.register(MyPlantLog,     MyPlantLogAdmin)
admin.site.register(MyPlantToDo,    MyPlantToDoAdmin)
admin.site.register(MyPlantComment, MyPlantCommentAdmin)
