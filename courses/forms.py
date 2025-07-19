from django import forms
from .models import Course

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'title', 'department', 'credit_hours']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean_code(self):
        code = self.cleaned_data['code']
        if not code.isupper():
            raise forms.ValidationError("Course code must be uppercase.")
        return code