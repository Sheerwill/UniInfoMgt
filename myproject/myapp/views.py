from django.contrib.auth.views import LoginView, PasswordResetView
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm, GraduationForm, ExamRegistrationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse, HttpResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from django.db.models import Q
from .models import Exams, StudentClassification
import csv
from django.contrib.auth.models import User
from django.contrib.messages import error
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError


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

'''def custom_reset_done_view(request):
    # Define your custom logic here, such as redirection to the root URL
    return redirect(reverse('custom_login'))'''

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
    return render(request, 'registration/signup.html', {'form': form})

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
                record_id = int(item['record_id'])
                percentage = int(item['percentage'])

                # Find the corresponding Exams record using the record_id
                exam = Exams.objects.get(pk=record_id)

                # Validate the percentage before updating the record
                if 0 <= percentage <= 100:
                    exam.percentage = percentage  # Update the percentage field
                    exam.save()  # Save the changes
                else:
                    return JsonResponse({'error': 'Invalid percentage value'})

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
    
def register_for_graduation(request):
    if request.method == 'POST':
        form = GraduationForm(request.POST)
        if form.is_valid():
            form.save() 
            return JsonResponse({'success': True})

        else:
            # Form is not valid, return 'false'
            return JsonResponse({'success': False})
    else:
        form = GraduationForm()

    # Render the form with or without error message
    return render(request, 'register_graduation.html', {'form': form})    


def register_for_exams(request):
    if request.method == 'POST':
        form = ExamRegistrationForm(request.POST)
        if form.is_valid():
            form.save() 
            return JsonResponse({'success': True})

        else:
            # Form is not valid, return 'false'
            return JsonResponse({'success': False})       

    else:
        form = ExamRegistrationForm()

    return render(request, 'register_exams.html', {'form': form})

@login_required
def graduation_search(request):
    # Student dashboard logic
    return render(request, 'graduation_status.html')

def query_student_classification(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode("utf-8"))
            student_id = data.get('student_id')
            program_id = data.get('program_id')

            if student_id and program_id:
                try:
                    student_classification = StudentClassification.objects.get(
                        student_id__student_number=student_id,
                        program_id__program_code=program_id
                    )
                except ObjectDoesNotExist:
                    return JsonResponse({'error': 'No data found for the given parameters'})
                
                # Serialize the student_classification object
                data = {
                    'faculty_id': student_classification.faculty_id.faculty_name,
                    'course_id': student_classification.course_id.course_name,
                    'program_id': student_classification.program_id.program_code,
                    'batch_id': student_classification.batch_id.batch_code,
                    'student_id': student_classification.student_id.student_name,
                    'average_marks': student_classification.average_marks,
                    'classification': student_classification.classification
                }
                return JsonResponse(data)
            else:
                return JsonResponse({'error': 'Missing or invalid parameters'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'})
    
    return JsonResponse({'error': 'Invalid request method'})

def export_csv(request):
    searchQuery = request.GET.get("searchQuery")    

    if searchQuery:
        # Filter the Exam model using the search query
        exams = Exams.objects.filter(unit_id__unit_code__exact=searchQuery)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="exam_results.csv"'

        writer = csv.writer(response)
        writer.writerow(['Unit Code', 'Student Name', 'Percentage', 'Grade', 'Remarks'])

        for exam in exams:
            writer.writerow([exam.unit_id.unit_code, exam.student_id.student_name, exam.percentage, exam.grade, exam.remarks])

        return response

    return HttpResponse("No data to export.")

def export_student_classification_to_csv(request):
    # Query the data you want to export
    data = StudentClassification.objects.all()

    # Create a CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="student_classification.csv"'

    # Create a CSV writer
    writer = csv.writer(response)
    writer.writerow(['Faculty', 'Course', 'Program', 'Batch', 'Student', 'Average Marks', 'Classification'])  # Header row

    for item in data:
        writer.writerow([
            item.faculty_id.faculty_name,
            item.course_id.course_name,
            item.program_id.program_code,
            item.batch_id.batch_code,
            item.student_id.student_name,
            item.average_marks,
            item.classification
        ])

    return response

class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'    
    template_name = 'registration/password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):        
        email = form.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            # Email doesn't exist in the database
            error(self.request, 'This email is not registered.')
            return self.render_to_response(
                self.get_context_data(form=form, unregistered_email=True)
            )
        return super().form_valid(form)