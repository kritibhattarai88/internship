import re
from django.shortcuts import render,redirect,get_object_or_404
from .models import Testimonial,Course,Blog
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from datetime import datetime
from django.core.mail import send_mail,EmailMessage
from django.contrib.auth.models import User


# Create your views here.
date = datetime.now().year

def base(request):
    return render(request, 'base.html')

def home(request):
    testimonials = Testimonial.objects.all()
    context = {
       
        "testimonials": testimonials,
    }
    return render(request, 'main/home.html',context)

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    if request.method == 'POST':
        name= request.POST['name']
        email= request.POST['email']
        purpose= request.POST['purpose']
        message= request.POST['message']

        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email):
            messages.error(request, "Invalid email")
            return redirect("contact")
        else:
            try:
                email_message = EmailMessage(
                subject='Form submission',
                body=message,
                from_email="bhattaraikriti.77@gmail.com",  # Your verified email address
                to=["bhattaraikriti.77@gmail.com"],  # Recipient's email address
                headers={"Reply-To": email}  # User's email in Reply-To header
            )
                email_message.send(fail_silently=False)
                messages.success(request, "Email has been sent!!")
                return redirect("home")
            except Exception as e:
                messages.error(request, f"Error sending email: {e}")
                return redirect("contact")

    return render(request, 'main/contact.html', {"date":date})

def course(request):
    course = Course.objects.all()
    context2={
        "courses":course,
        "date":date,
    }
    return render(request, 'main/course.html',context2)

# def blog(request):
    
#     return render(request, 'main/blog.html')
def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'main/blog_list.html', {'blogs': blogs, 'date':date})

def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, 'main/blog_detail.html', {'blog': blog, 'date':date})

# +++++======Authentication section======+++++++++++

from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')  # Success message
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')  # Error message
    return render(request, 'userauthentication/login.html')

def register_view(request):
    if request.method == 'POST':
        # Extract data from the POST request
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Check if passwords match
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')  # Error message
            return redirect('register')

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')  # Error message
            return redirect('register')

        # Check if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')  # Error message
            return redirect('register')

        # Create the user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        messages.success(request, 'Registration successful. Please log in.')  # Success message
        return redirect('login')
    else:
        # Render the registration form
        return render(request, 'userauthentication/register.html')

def logout_view(request):
    logout(request)  # Logs out the user
    messages.success(request, 'You have been successfully logged out.')  # Success message
    return redirect('home')  # Redirect to the homepage
