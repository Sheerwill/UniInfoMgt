from django.urls import path
from .views import (CustomLoginView, staff_dashboard_view, student_dashboard_view, signup,
                    search_exams, custom_logout, PostPercentagesView)


urlpatterns = [
    path('', CustomLoginView.as_view(), name='custom_login'),    
    path('student/', student_dashboard_view, name='student_dashboard'),
    path('signup/', signup, name='signup'),
    path('staff/', staff_dashboard_view, name='staff_dashboard'), 
    path('search/', search_exams, name='search_exams'), 
    path('logout/', custom_logout, name='logout'),   
    path('post_percentages/', PostPercentagesView.as_view(), name='post_percentages'),  
    path('search-exams/', search_exams, name='search_exams'), #For students
]