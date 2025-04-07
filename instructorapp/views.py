from django.shortcuts import render,redirect
from myapp.models import *
# Create your views here.
def instructordashboard(request):
    return render(request, "instructor/instructordashboard.html")
def create_course(request):
    if request.method=="POST":
        title= request.POST['name']
        description=request.POST['description']
        prerequisites=request.POST['prerequisites']
        skill_level=request.POST['skill_level']
        duration=request.POST['duration']
        fee=request.POST['fee']
        image=request.FILES.get('image')
        instructor=request.user

        Course.objects.create(name=title, description=description, prerequisites=prerequisites, skill_level=skill_level, duration=duration, fee=fee, image=image, instructor=instructor)
        
        return redirect('course')
    return render(request, 'instructor/create_course.html')

def mycourse(request):
    courses = Course.objects.filter(instructor=request.user)
    return render(request, 'instructor/mycourse.html', {'courses': courses})