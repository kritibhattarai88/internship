import re
import uuid

from django.http import JsonResponse
from django.urls import reverse
import requests
from .models import *
from datetime import datetime
from django.shortcuts import render,redirect,get_object_or_404
from .models import Testimonial,Course,Blog
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.core.mail import send_mail,EmailMessage
from django.contrib.auth.models import User
# Create your views here.

KHALTI_SECRET_KEY = "1d5b383adc3a41f3bbe012a1a5128228"
KHALTI_INITIATE_URL = "https://dev.khalti.com/api/v2/epayment/initiate/"

date = datetime.now().year

def base(request):
    return render(request, 'base.html',{'date':date})

def home(request):
    testimonials = Testimonial.objects.all()
    courses= Course.objects.all()
    context = {
        "courses":courses,
        "testimonials": testimonials,
        "date":date,
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


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successfully!')  # Success message
            if user.user_type=="student":
              return redirect('home')
            elif user.user_type=="instructor":
                return redirect('instructordashboard')
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
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')  # Error message
            return redirect('register')

        # Check if email already exists
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')  # Error message
            return redirect('register')

        # Create the user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            user_type='student'
            
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

def payment(request ,id):
    course=Course.objects.get(id=id)
    transaction_id = uuid.uuid4().hex
    return render(request, 'main/payment.html', {'course':course, 'transaction_id':transaction_id})

def initkhalti(request):
    if request.method == "POST":
        print(f"POST data: {request.POST}")
        purchase_order_id = request.POST.get("purchase_order_id")
        fee = int(float(request.POST.get("amount")) * 100)  # Convert NPR to Paisa
        course_id = request.POST.get("course_id")

        # Store course_id in session to use it later
        request.session["course_id"] = course_id

        return_url = request.build_absolute_uri(reverse("khalti_success"))

        payload = {
            "return_url": return_url,
            "website_url": request.build_absolute_uri("/"),
            "amount": fee,
            "purchase_order_id": purchase_order_id,
            "purchase_order_name": "Course Payment",
        }

        headers = {"Authorization": f"Key {KHALTI_SECRET_KEY}"}

        response = requests.post(KHALTI_INITIATE_URL, json=payload, headers=headers)
        response_data = response.json()

        if response.status_code == 200 and "payment_url" in response_data:
            khalti_payment_url = response_data["payment_url"]
            return redirect(khalti_payment_url)
        else:
            return JsonResponse({"error": "Khalti Payment Failed"}, status=400)

    return redirect("course")  # Redirect back if method is not POST

def khalti_payment_success(request):
    token = request.GET.get("pidx")  # Khalti's payment token

    if not token:
        return JsonResponse({"error": "Invalid payment details."}, status=400)

    verification_url = "https://dev.khalti.com/api/v2/epayment/lookup/"
    headers = {
        "Authorization": f"Key {KHALTI_SECRET_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"pidx": token}

    try:
        response = requests.post(verification_url, headers=headers, json=payload)

        # Check if the response is valid JSON
        try:
            response_data = response.json()
            print("Khalti API Response:", response_data)  # Debugging
        except ValueError:
            return JsonResponse(
                {"error": "Invalid response from Khalti API."}, status=500
            )

        # Handle the response based on the state
        if response.status_code == 200 and response_data.get("status") == "Completed":
            # Assuming the course ID is passed through session or another method
            course_id = request.session.get("course_id")
            print(f"Retrieved course_id from session: {course_id}")  # Debugging
            if not course_id:
                return render(
                    request,
                    "main/paymentfailure.html",
                    {"error": "Course not found in session."},
                )

            course = Course.objects.get(id=course_id)

            # Create or update the payment record
            payment = Payment.objects.create(
                transaction_id=token,
                user=request.user,
                course=course,
                amount=course.fee,  # Assuming the course.discount contains the correct amount
                payment_method="khalti",
                status="completed",  # Mark the payment as completed
            )

            # Render the success page
            return render(request, "main/paymentsuccess.html", {"payment": payment})

        else:
            return render(
                request,
                "main/paymentfailure.html",
                {"error": "Payment verification failed."},
            )

    except requests.exceptions.RequestException as e:
        return render(
            request,
            "main/paymentfailure.html",
            {"error": f"Request failed: {str(e)}"},
        )
    except Exception as e:
        return render(
            request,
            "main/paymentfailure.html",
            {"error": f"An error occurred: {str(e)}"},
        )