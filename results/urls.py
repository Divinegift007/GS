from django.urls import path
from .views import (
    ResultListView,
    #generate_transcript_pdf,
    ResultUpdateView,
    GradebookView, 
)

urlpatterns = [
    path('', ResultListView.as_view(), name='result-list'),
    path('<int:pk>/edit/', ResultUpdateView.as_view(), name='result-update'),
    #path('<int:enrollment_id>/edit/', ResultUpdateView.as_view(), name='result-update'),
    path('gradebook/<int:course_id>/', GradebookView.as_view(), name='gradebook'),
    
    # PDF Generation
    #path('transcript/<int:student_id>/', generate_transcript_pdf, name='generate-transcript'),
]


