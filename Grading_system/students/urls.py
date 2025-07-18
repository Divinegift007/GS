from django.urls import path
from .views import (
    StudentListView,
    StudentDetailView,
    StudentCreateView,
    StudentUpdateView,
    DepartmentListView,
    EnrollmentCreateView,
    #StudentEnrollmentView
)

urlpatterns = [
    path('', StudentListView.as_view(), name='student-list'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('new/', StudentCreateView.as_view(), name='student-create'),
    path('<int:pk>/edit/', StudentUpdateView.as_view(), name='student-update'),

    #Enroll course
    path('enroll/', EnrollmentCreateView.as_view(), name='enroll-course'),
    
    #path('enroll/', StudentEnrollmentView.as_view(), name='enroll-course'),
    
    # Department URLs
    path('departments/', DepartmentListView.as_view(), name='department-list'),
]