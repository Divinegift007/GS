from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, FormView
from .models import Student, Department
from django.urls import reverse_lazy
from .forms import EnrollmentForm, ProfileSetupForm
from courses.models import Course
from .models import Enrollment
from django.contrib import messages

# Create your views here.

class StudentListView(LoginRequiredMixin, ListView):
    model = Student
    template_name = 'students/list.html'

    def get_queryset(self):
        if self.request.user.is_teacher:
            return Student.objects.all()
        return Student.objects.filter(user=self.request.user)
    
class StudentDetailView(DetailView):    
    model = Student
    template_name = 'students/detail.html'

class StudentCreateView(CreateView):
    model = Student
    fields = ['user', 'department', 'level']  
    template_name = 'students/form.html'

class StudentUpdateView(UpdateView):
    model = Student
    fields = ['user', 'department', 'level'] 
    template_name = 'students/form.html'

class DepartmentListView(ListView):
    model = Department
    template_name = 'students/department_list.html'


class StudentProfileSetupView(LoginRequiredMixin, FormView):
    template_name = 'students/profile_setup.html'
    form_class = ProfileSetupForm
    success_url = reverse_lazy('student-dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self.request.user, 'student'):
            kwargs['instance'] = self.request.user.student
        return kwargs

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "Profile updated successfully!")
        return super().form_valid(form)

class EnrollmentCreateView(CreateView):
    form_class = EnrollmentForm
    template_name = 'students/enroll_course.html'
    success_url = reverse_lazy('student-dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if hasattr(self.request.user, 'student'):
            kwargs['student'] = self.request.user.student
        return kwargs

    def form_valid(self, form):
        if hasattr(self.request.user, 'student'):
            enrollment = form.save(commit=False)
            enrollment.student = self.request.user.student
            enrollment.save()
            messages.success(self.request, f"Successfully enrolled in {form.cleaned_data['course'].title}")
            return super().form_valid(form)
        messages.error(self.request, "Student profile not found")
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = self.get_form()
        context['has_courses'] = form.fields['course'].queryset.exists() if 'course' in form.fields else False
        return context