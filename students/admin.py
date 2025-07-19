from django.contrib import admin
from .models import Student, Enrollment

# Register your models here


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'matric_number', 'student_id', 'department', 'admission_date']
    search_fields = ['full_name', 'matric_number', 'student_id']

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date', 'grade')
    list_filter = ('course', 'grade')
    search_fields = ('student__username', 'course__title')