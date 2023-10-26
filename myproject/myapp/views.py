from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Faculties

class CustomLoginView(LoginView):
    def form_valid(self, form):
        # Call the parent class's form_valid method
        super().form_valid(form)
        
        # Check if the user is staff
        if self.request.user.is_staff:
            return redirect('staff_dashboard')  # Redirect to staff dashboard
        else:
            return redirect('student_dashboard')  # Redirect to student dashboard

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


class FacultyListView(ListView):
    model = Faculties
    template_name = 'faculty_list.html'
    context_object_name = 'faculties'

class FacultyCreateView(CreateView):
    model = Faculties
    template_name = 'faculty_form.html'
    fields = '__all__'
    success_url = 'staff/' 

class FacultyUpdateView(UpdateView):
    model = Faculties
    template_name = 'faculty_form.html'
    fields = '__all__'
    success_url = 'staff/'

class FacultyDeleteView(DeleteView):
    model = Faculties
    template_name = 'faculty_confirm_delete.html'
    success_url = 'staff/'
