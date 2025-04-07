from django.urls import path
from .views import * 
urlpatterns = [
    path("", instructordashboard, name="instructordashboard"),
    path("create_course/", create_course, name="create_course"),
    path("mycourse/", mycourse, name="mycourse")
]
