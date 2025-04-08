from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.conf import settings
# Create your models here.

class CustomUser(AbstractUser):
    USER_TYPE = (
        ("student", "Student"),
        ("instructor", "Instructor"),
    )
    
    user_type = models.CharField(max_length=100, choices=USER_TYPE)
    instructor_applied = models.BooleanField(default=False)
    instructor_approved = models.BooleanField(default=False) 
    is_active = models.BooleanField(default=True) 
    user_profile_image = models.ImageField(upload_to="images/profile_images/")
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
    
class Testimonial(models.Model):
    student_name = models.CharField(max_length=100)
    postion = models.CharField(max_length=100)
    testimonial = models.TextField()
    photo = models.ImageField(upload_to="testimonials/",null=True,blank=True)
    rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=0.0
    )  # Max 5.0 rating
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.student_name
    
class Course(models.Model):
    SKILL_LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    DURATION_CHOICES = [
        ('short-term', 'Short-term'),
        ('long-term', 'Long-term'),
    ]
    instructor = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    null=True,  
    blank=True, 
    related_name='courses'
)
    name = models.CharField(max_length=200)
    old_fee = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    description = models.TextField()
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES)
    prerequisites = models.TextField(blank=True)
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    
    

    def __str__(self):
        return self.name 

class Blog(models.Model):
    CATEGORY_CHOICES = [
        ('trends', 'IT Industry Trends'),
        ('learning-tips', 'Learning Tips for Programming'),
        ('career-guidance', 'Career Guidance in Tech Fields'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
    
class Payment(models.Model):
    PAYMENT_METHODS = [
        ("esewa", "eSewa"),
        ("khalti", "Khalti")
    ]
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, unique=True,null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def str(self):
        return f"{self.user.username} - {self.course.title} - {self.payment_method} - {self.status}"