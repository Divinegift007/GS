from django.db import models
from django.conf import settings
from departments.models import Department

class Course(models.Model):
    code = models.CharField(max_length=10, unique=True)
    title = models.CharField(max_length=200)
    department = models.ForeignKey('departments.Department', on_delete=models.CASCADE)
    credit_hours = models.PositiveIntegerField(default=3)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses_created'
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='courses_taught'
    )

    def __str__(self):
        return f"{self.code} - {self.title}"

    