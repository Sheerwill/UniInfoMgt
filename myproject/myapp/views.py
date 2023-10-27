from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Exams
from django.http import JsonResponse, request
from django.core import serializers
from django.urls import reverse

class CustomLoginView(LoginView):
    def form_valid(self, form):
        # Call the parent class's form_valid method
        super().form_valid(form)
        
        # Check if the user is staff
        if self.request.user.is_staff:
            return redirect('staff_dashboard')  # Redirect to staff dashboard
        else:
            return redirect('student_dashboard')  # Redirect to student dashboard        


def custom_logout(request):
    logout(request)
    return redirect(reverse('custom_login'))

# Define a custom check to identify staff users
def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def staff_dashboard_view(request):
    # Staff dashboard logic
    return render(request, 'staff_dashboard.html')

def student_dashboard_view(request):
    # Student dashboard logic
    return render(request, 'student_dashboard.html')

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')  
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

@login_required
@user_passes_test(is_staff)
def search_exams(request):    
        search_query = request.GET.get("search_query")
        if search_query:
            # Perform a search based on the related model's attribute
            results = Exams.objects.filter(unit_id__unit_code__exact=search_query)
        else:
            # If no query provided
            results = []

        if results:
            # Serialize the queryset results to JSON
            results_data = [{
                'unit_code': result.unit_id.unit_code,
                'student_id': result.student_id.student_name,
                'percentage': result.percentage,
                'grade': result.grade,
                'remarks': result.remarks
            } for result in results]
        else:
            results_data = []  # Empty list if no results

        return JsonResponse({'results': results_data})   