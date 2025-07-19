from django.db import models
from django.conf import settings
from departments.models import Department

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=150, blank=True)
    matric_number = models.CharField(max_length=20, unique=True, null=True, blank=True)
    student_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE, null=True, blank=True)
    admission_date = models.DateField(null=True, blank=True)
    LEVEL_CHOICES = [
        ('100', '100 Level'),
        ('200', '200 Level'),
        ('300', '300 Level'),
        ('400', '400 Level'),
        ('500', '500 Level'),
    ]
    
    level = models.CharField(max_length=3, choices=LEVEL_CHOICES, default='100')
    

    def __str__(self):
        return self.full_name or self.user.username

class Enrollment(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)
    semester = models.CharField(max_length=20)
    academic_year = models.CharField(max_length=9)
    grade = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        unique_together = [['student', 'course']]
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'

    def __str__(self):
       return f"{self.student} in {self.course} ({self.semester} {self.academic_year})"