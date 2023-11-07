from django.urls import path, include
from .views import (CustomLoginView, staff_dashboard_view, student_dashboard_view, signup,
                    search_exams, search_examinations, custom_logout, PostPercentagesView,
                    register_for_graduation, register_for_exams, graduation_search,
                    query_student_classification, export_student_classification_to_csv, export_csv,
                    )
from django.contrib.auth.views import PasswordResetCompleteView, PasswordResetDoneView


urlpatterns = [
    path('', CustomLoginView.as_view(), name='custom_login'),    
    path('student/', student_dashboard_view, name='student_dashboard'),
    path('signup/', signup, name='signup'),
    path('staff/', staff_dashboard_view, name='staff_dashboard'), 
    path('search/', search_examinations, name='search_exams'), #Staff
    path('logout/', custom_logout, name='logout'),   
    path('post_percentages/', PostPercentagesView.as_view(), name='post_percentages'),  
    path('search-exams/', search_exams, name='search_exams'), #For students
    path('register-graduation/', register_for_graduation, name='register-graduation'),
    path('register-exams/', register_for_exams, name='register-exams'),
    path('search_graduation/', graduation_search, name='search_graduation'),
    path('query-student-classification/', query_student_classification, name='query_student_classification'),
    path('export-student-classification/', export_student_classification_to_csv, name='export_student_classification_to_csv'),
    path('export-csv/', export_csv, name='export_csv'),
    
    path('accounts/', include('django.contrib.auth.urls')),    
]
