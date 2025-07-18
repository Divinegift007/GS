from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, UpdateView
from .models import Result
from students.models import Enrollment
from django.urls import reverse_lazy

class ResultListView(LoginRequiredMixin, ListView):
    model = Result
    template_name = 'results/result_list.html'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_student:
            return queryset.filter(enrollment__student__user=self.request.user)
        return queryset

class ResultUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Result
    fields = ['quiz', 'test', 'exam']  #only these fields are editable
    template_name = 'results/result_update.html'
    
    def test_func(self):
        return self.request.user.is_teacher
    
    def get_success_url(self):
        # Redirect back to the course gradebook
        return reverse_lazy('gradebook', kwargs={
            'course_id': self.object.enrollment.course.id
        })
    
    

class GradebookView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Enrollment
    template_name = 'results/gradebook.html'
    context_object_name = 'enrollments'
    
    def test_func(self):
        return self.request.user.is_teacher
    
    def get_queryset(self):
        self.course_id = self.kwargs['course_id']
        queryset = Enrollment.objects.filter(
            course_id=self.course_id
        ).select_related('student__user', 'course')
        
        # Ensure each enrollment has a corresponding Result
        for enrollment in queryset:
            result, created = Result.objects.get_or_create(enrollment=enrollment)
            enrollment.result = result  # attach for template access

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.object_list.exists():
            context['course'] = self.object_list.first().course
        return context


"""
from django.shortcuts import render
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import DetailView, ListView, UpdateView
from .models import Result


# Create your views here.

class ResultDetailView(UserPassesTestMixin, DetailView):
    def test_func(self):
        user = self.request.user
        result = self.get_object()
        return user.is_teacher or (user.is_student and result.student.user == user)
    
###
class ResultListView(ListView):
    model = Result
    template_name = 'results/result_list.html'

class ResultUpdateView(UpdateView):
    model = Result
    fields = ['grade']  
    template_name = 'results/result_update.html'



from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from students.models import Student

def generate_transcript(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    html = render_to_string('results/transcript_pdf.html', {'student': student})
    pdf = HTML(string=html).write_pdf()
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'filename=transcript_{student.student_id}.pdf'
    return response

"""