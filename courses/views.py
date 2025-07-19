from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.urls import reverse_lazy
from .models import Course
from students.models import Enrollment
from .forms import CourseForm
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

@user_passes_test(lambda u: u.is_teacher)
def grade_course(request, course_id):
    course = get_object_or_404(course, pk=course_id)
    # Add grading logic here
    return render(request, 'courses/grade_course.html', {'course': course})


class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'

class EnrollmentListView(ListView):
    model = Enrollment
    template_name = 'courses/enrollment_list.html'

class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('course-list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user  # Track creator
        return super().form_valid(form)

"""
class GradebookView(TemplateView):
    template_name = 'courses/gradebook.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add gradebook logic here
            return context """
        
def gradebook(request, course_id):
        course = get_object_or_404(Course, pk=course_id)
        enrollments = Enrollment.objects.filter(course=course)
        return render(request, 'courses/gradebook.html', {'course': course, 'enrollments': enrollments})