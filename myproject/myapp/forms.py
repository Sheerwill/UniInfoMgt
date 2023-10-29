from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import StudentClassification, Exams

class SignupForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class GraduationForm(forms.ModelForm):
    class Meta:
        model = StudentClassification
        fields = ['faculty_id', 'course_id', 'program_id', 'batch_id', 'student_id']

class ExamRegistrationForm(forms.ModelForm):
    class Meta:
        model = Exams
        fields = ['unit_id', 'student_id']
