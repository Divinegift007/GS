from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from students.models import Enrollment

# Create your models here.

class Result(models.Model):
    GRADE_CHOICES = [
        ('A', 'Excellent'),
        ('B', 'Very Good'),
        ('C', 'Good'),
        ('D', 'Pass'),
        ('E', 'Weak Pass'),
        ('F', 'Fail'),
    ]

    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE)
    quiz = models.DecimalField(max_digits=4, decimal_places=2, default=0, validators=[MinValueValidator(0.00), MaxValueValidator(20.00)])
    test = models.DecimalField(max_digits=4, decimal_places=2, default=0, validators=[MinValueValidator(0.00), MaxValueValidator(20.00)])
    exam = models.DecimalField(max_digits=4, decimal_places=2, default=0, validators=[MinValueValidator(0.00), MaxValueValidator(60.00)])
    total = models.DecimalField(max_digits=5, decimal_places=2, editable=False)
    grade = models.CharField(max_length=1, choices=GRADE_CHOICES, editable=False)

    def save(self, *args, **kwargs):
        self.total = (self.quiz) + (self.test) + (self.exam)
        self.grade = self.calculate_grade()
        super().save(*args, **kwargs)

    def calculate_grade(self):
        if self.total >= 70: return 'A'
        elif self.total >= 60: return 'B'
        elif self.total >= 50: return 'C'
        elif self.total >= 45: return 'D'
        elif self.total >= 40: return 'E'
        return 'F'