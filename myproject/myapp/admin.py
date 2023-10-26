from django.contrib import admin
from .models import Faculties, Courses, Programs, Batches

class FacultiesAdmin(admin.ModelAdmin):
    # Define fields to be displayed in the admin panel
    list_display = ('faculty_code', 'faculty_name')

    # Define fields that can be left blank in the admin panel
    exclude = ('faculty_head_id', 'student_id', 'lecturer_id', 'course_id')

# Register your models here.
admin.site.register(Faculties, FacultiesAdmin)
admin.site.register(Courses)
admin.site.register(Programs)
admin.site.register(Batches)


