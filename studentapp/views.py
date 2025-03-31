from django.shortcuts import render
from .models import *
# Create your views here.
def dashboard(request):
    return render(request, 'dashboard/dashboard.html')
def profile(request):
    return render(request,'dashboard/profile.html',{'user':request.user})
def job_announcement(request):
    jobs = JobAnnouncement.objects.all()
    return render(request, 'dashboard/job.html',{'jobs':jobs})

