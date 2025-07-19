from django.urls import path
from .views import (
    CourseListView,
    CourseDetailView,
    EnrollmentListView,
    gradebook,
    CourseCreateView
)
from courses import views

urlpatterns = [
    path('', CourseListView.as_view(), name='course-list'),
    path('<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    
    # Course creation URL
    path('add/', CourseCreateView.as_view(), name='course-add'),
    
    # Enrollment URLs
    path('enrollments/', EnrollmentListView.as_view(), name='enrollment-list'),
    
    # Gradebook URL
    path('<int:course_id>/gradebook/', views.gradebook, name='gradebook'),
    #path('<int:course_id>/gradebook/', GradebookView.as_view(), name='gradebook'),
    # path('courses/gradebook/', views.gradebook, name='gradebook'),
]