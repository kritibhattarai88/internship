from django.urls import path
from .views import * 
urlpatterns = [
    path("", instructordashboard, name="instructordashboard"),
    path("create_course/", create_course, name="create_course"),
    path("mycourse/", mycourse, name="mycourse"),
    path("view_course/<int:pk>/", view_course, name="view_course"),
    path("edit_course/<int:pk>/", edit_course, name="edit_course"),
   
]
