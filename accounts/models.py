from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


# Create your models here.

class User(AbstractUser):
    is_student = models.BooleanField(default=True)  # Default to student
    is_teacher = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_teacher and not self.pk:
            self.is_staff = True  # Grant admin access
        super().save(*args, **kwargs)
        


    def clean(self):
        if self.is_student and self.is_teacher:
            raise ValidationError("User cannot be both student and teacher")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True)
    birth_date = models.DateField(null=True, blank=True)

