from django.shortcuts import render,redirect

# Create your views here.
def instructordashboard(request):
    return render(request, "instructor/instructordashboard.html")