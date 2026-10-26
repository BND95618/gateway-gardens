# /app/myplants/urls.py 
"""
URL mapping for the Plants App
"""
from django.urls import path
from myplants    import views

app_name = "myplants"
urlpatterns = [
    path('myplants_summary/',           views.myplants_summary,  name='myplants_summary'),
    path('my_column_chooser/',          views.my_column_chooser, name='my_column_chooser'),
    #
    path('myplant_status/<int:id>/',    views.myplant_status,    name='myplant_status'),
    path('myplant_details/<int:id>/',   views.myplant_details,   name='myplant_details'),
    path('myplant_add/<int:id>/',       views.myplant_add,       name='myplant_add'),
    path('myplant_edit/<int:id>/',      views.myplant_update,    name='myplant_update'),
    path('myplant_delete/<int:id>/',    views.myplant_delete,    name='myplant_delete'),
    #
    path('myplant_log_add/<int:id>/',   views.myplant_log_add,   name='myplant_log_add'),
    path('myplant_log_edit/<int:id>/',  views.myplant_log_edit,  name='myplant_log_edit'),
    path('myplant_log_del/<int:id>/',   views.myplant_log_del,   name='myplant_log_del'),
    #
    path('myplant_todo_add/<int:id>/',  views.myplant_todo_add,  name='myplant_todo_add'),
    path('myplant_todo_edit/<int:id>/', views.myplant_todo_edit, name='myplant_todo_edit'),
    path('myplant_todo_del/<int:id>/',  views.myplant_todo_del,  name='myplant_todo_del'),
    path('myplant_todo_done/<int:id>/', views.myplant_todo_done, name='myplant_todo_done'),
    path('myplant_todo_save/<int:id>/', views.myplant_todo_save, name='myplant_todo_save'),
    #
    path('myplant_comment/<int:id>/',   views.myplant_comment,   name='myplant_comment'),
]