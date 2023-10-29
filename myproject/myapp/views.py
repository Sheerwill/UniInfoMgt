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
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.db.models import Q

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

@login_required
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
            return redirect('student_dashboard')  
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

@login_required
@user_passes_test(is_staff)
def search_examinations(request):    
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
            'id': result.id,  # Include the ID field
            'unit_code': result.unit_id.unit_code,
            'student_id': result.student_id.student_name,
            'percentage': result.percentage,
            'grade': result.grade,
            'remarks': result.remarks
        } for result in results]
    else:
        results_data = []  # Empty list if no results

    return JsonResponse({'results': results_data})  


@method_decorator(csrf_exempt, name='dispatch')
class PostPercentagesView(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))  # Parse the JSON data            
            for item in data["data"]:
                print(json.dumps(data, indent=4))                
                record_id = int(item['record_id'])
                percentage = int(item['percentage'])

                # Find the corresponding Exams record using the record_id
                exam = Exams.objects.get(pk=record_id)
                exam.percentage = percentage  # Update the percentage field
                exam.save()  # Save the changes

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'error': str(e)})

#Student's portal
@login_required
def search_exams(request):
    if request.method == "POST":
        # Get the data from the request body
        data = json.loads(request.body.decode("utf-8"))
        selected_session = data.get("session")
        student_number = data.get("studentNumber")

        print(selected_session, student_number)

        # Query the database using the received data
        if selected_session and student_number:
            exams = Exams.objects.filter(
                Q(student_id__student_number__iexact=student_number) &
                Q(unit_id__time_id__time_code__iexact=selected_session)
            )
        else:
            exams = Exams.objects.none()  # Return an empty result set

        # Prepare the search results as JSON
        search_results = []
        for exam in exams:
            search_results.append({
                "student_id": {"student_number": exam.student_id.student_number},
                "unit_id": {"unit_name": exam.unit_id.unit_name},
                "grade": exam.grade,
                "remarks": exam.remarks,
            })

        return JsonResponse(search_results, safe=False)  # Return search results as JSON   