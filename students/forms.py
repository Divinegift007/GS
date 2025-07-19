from django import forms
from courses.models import Course
from .models import Student, Enrollment

class ProfileSetupForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['full_name', 'matric_number', 'student_id', 'department', 'admission_date']

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['course', 'semester', 'academic_year']
        
    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super().__init__(*args, **kwargs)
        if student:
            # Exclude courses already enrolled in
            enrolled_courses = Enrollment.objects.filter(student=student).values_list('course', flat=True)
            self.fields['course'].queryset = Course.objects.exclude(id__in=enrolled_courses)
            self.fields['course'].label_from_instance = lambda obj: f"{obj.code} - {obj.title}"
