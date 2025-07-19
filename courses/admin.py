from django.contrib import admin
#from .models import Course, Enrollment, Department
from .models import Course 

# Register your models here.

"""
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name') 
    """


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'department',)
    search_fields = ('code', 'title')
    list_filter = ('department', 'teacher')

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.created_by = request.user
            super().save_model(request, obj, form, change)