from django.urls import path
from .views import CustomLoginView, staff_dashboard_view, student_dashboard_view, signup
from .views import FacultyListView, FacultyCreateView, FacultyUpdateView, FacultyDeleteView

urlpatterns = [
    path('', CustomLoginView.as_view(), name='custom_login'),    
    path('student_dashboard/', student_dashboard_view, name='student_dashboard'),
    path('signup/', signup, name='signup'),

    path('staff/', staff_dashboard_view, name='staff_dashboard'),
    path('staff/faculties/', FacultyListView.as_view(), name='faculty_list'),
    path('staff/faculties/add/', FacultyCreateView.as_view(), name='faculty_add'),
    path('staff/faculties/<int:pk>/', FacultyUpdateView.as_view(), name='faculty_update'),
    path('staff/faculties/<int:pk>/delete/', FacultyDeleteView.as_view(), name='faculty_delete'),
]