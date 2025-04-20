from django.urls import path
from .views import *

urlpatterns = [
    path("base/",base, name='base'),
    path("",home, name='home'),
    path("about/", about, name='about'),
    path("contact/", contact, name='contact'),
    path("course/",course, name='course'),
    path("blog/", blog_list,name='blog_list'),
    path('blog/<slug:slug>/', blog_detail, name='blog_detail'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path("payment/<int:id>", payment, name="payment"),
    path("initiate/", initkhalti, name="initiate"),
    path("khalti/paymentsuccess", khalti_payment_success, name="khalti_success")
  
  
    
]
