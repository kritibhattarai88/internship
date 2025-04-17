from django.shortcuts import render,redirect, get_object_or_404
from myapp.models import Course
from .forms import CourseForm

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

def view_course(request, pk):
    course = get_object_or_404(Course, pk=pk, instructor=request.user)
    return render(request, 'instructor/view_course.html', {'course': course})

def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk, instructor=request.user)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            return redirect('view_course', pk=course.pk)
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'instructor/edit_course.html', {
        'form': form,
        'course': course
    })
