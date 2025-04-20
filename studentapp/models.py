from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class JobAnnouncement(models.Model):
    JOB_TYPE_CHOICES = [
        ('fulltime', 'Full-Time'),
        ('shorttime', 'Short-Time'),
    ]

    CATEGORY_CHOICES = [
        ('software_dev', 'Software Development'),
        ('data_science', 'Data Science'),
        ('cybersecurity', 'Cybersecurity'),
        ('networking', 'Networking & Infrastructure'),
        ('ai_ml', 'AI & Machine Learning'),
        ('cloud_computing', 'Cloud Computing'),
        ('it_support', 'IT Support & Administration'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    location = models.CharField(max_length=255)
    description = models.TextField()
    job_type = models.CharField(max_length=10, choices=JOB_TYPE_CHOICES, default='fulltime')
    posted_at = models.DateTimeField(auto_now_add=True)
    application_deadline = models.DateField()
    email = models.EmailField()

    def __str__(self):
        return f"{self.title} at {self.company}"
    
