from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    is_student = forms.BooleanField(
        required=False,
        initial=True,  # Default checked (student)
        label="I am a student (uncheck if you're a teacher)",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = self.cleaned_data['is_student']
        user.is_teacher = not user.is_student  # Automatically set teacher status
        if commit:
            user.save()
        return user