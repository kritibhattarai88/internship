from django.urls import path
from .views import *
urlpatterns = [
    path("dashboard/", dashboard, name='dashboard'),
    path("profile/", profile, name='profile'),
    path("job_placement", job_placement, name='job_placement')
]
