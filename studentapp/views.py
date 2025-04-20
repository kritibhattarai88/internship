import re
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from myapp.models import *
from django.core.mail import EmailMessage
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def dashboard(request):
    context = {
        'user': request.user  
    }
    return render(request, 'dashboard/dashboard.html', context)
def profile(request):
    return render(request,'dashboard/profile.html',{'user':request.user})
def job_announcement(request):
    jobs = JobAnnouncement.objects.all()
    return render(request, 'dashboard/job.html',{'jobs':jobs})

def become_instructor(request):
    if request.method == 'POST':
        try:
            # Prepare email content
            subject = 'New Instructor Application'
            message = f'User {request.user.username} ({request.user.email}) wants to become an instructor.'
            
            email_message = EmailMessage(
                subject=subject,
                body=message,
                from_email="bhattaraikriti.77@gmail.com",
                to=["bhattaraikriti.77@gmail.com"],
                headers={"Reply-To": request.user.email}
            )
            email_message.send(fail_silently=False)
           
            # Update user status
            request.user.instructor_applied = True
            request.user.save()
            
            messages.success(
                request,
                "Your instructor application has been submitted successfully! "
                "Our team will review your request and contact you soon."
            )
            return redirect('dashboard')  # Redirect to regular dashboard until approved
            
        except Exception as e:
            messages.error(
                request,
                f"We couldn't process your request right now. Error: {e} "
                "Please try again later or contact support."
            )
            return redirect('dashboard')
    
    return redirect('dashboard')

@login_required
def enrolled_courses(request):
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    return render(request, 'dashboard/enrolled_courses.html', {
        'enrollments': enrollments
    })

def course_player(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    # Check if user is enrolled (optional security check)
    if not request.user.is_authenticated or not course.enrollment_set.filter(student=request.user).exists():
        return redirect('enrolled_courses')
    
    return render(request, 'dashboard/course_player.html', {
        'course': course,
        'enrolled': True
    })