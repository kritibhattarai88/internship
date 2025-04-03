from django.urls import path
from .views import *
urlpatterns = [
    path("dashboard/", dashboard, name='dashboard'),
    path("profile/", profile, name='profile'),
    path("job_announcement/", job_announcement, name='job_announcement'),
    path("become_instructor/", become_instructor, name="become_instructor"),
    
]
