from django.urls import path
from .views import (CustomLoginView, staff_dashboard_view, student_dashboard_view, signup,
                    search_exams, search_examinations, custom_logout, PostPercentagesView, register_for_graduation)


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
]