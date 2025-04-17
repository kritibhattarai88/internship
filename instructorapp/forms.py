from django import forms
from myapp.models import Course


class CourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        self.fields['description'].widget.attrs['rows'] = 4

    class Meta:
        model = Course
        fields = ['name', 'description', 'duration', 'skill_level', 'image']
        labels = {
            'name': 'Course Name',
            'description': 'Course Description',
            'image': 'Course Image'
        }
        help_texts = {
            'image': 'Upload a high-quality image for your course'
        }