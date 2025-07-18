from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from students.models import Student, Enrollment
from courses.models import Course
from results.models import Result
from django.db.models import Sum, Case, When, FloatField, F
from .models import Profile
from django.contrib import messages
from students.forms import ProfileSetupForm

# Views.

#Registration View
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create profile automatically
            Profile.objects.create(user=user)
            
            # Create Student or Teacher profile based on selection
            if user.is_student:
                Student.objects.create(user=user)
                messages.success(request, "Student account created successfully!")
            else:
                messages.success(request, "Teacher account created successfully!")
                
            login(request, user)
            return redirect('dashboard')
        else:
            # Print form errors to console for debugging
            print("Form errors:", form.errors)
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required    
def dashboard(request):
    # Student Dashboard
    if request.user.is_student:
        try:
            student = request.user.student
            enrollments = Enrollment.objects.filter(student=student).select_related('course', 'result')
            context = {
                'role': 'student',
                'student': student,
                'enrollments': enrollments,
                'cgpa': calculate_cgpa(enrollments),
            }
        except Student.DoesNotExist:
            messages.error(request, "Student profile missing!")
            return redirect('profile_setup')

    # Teacher Dashboard
    elif request.user.is_teacher:
        courses = Course.objects.filter(teacher=request.user)
        context = {
            'role': 'teacher',
            'courses': courses,
            'student_count': sum(c.enrollments.count() for c in courses)
        }
        
    # Admin Dashboard
    elif request.user.is_superuser:
        context = {
            'role': 'admin',
            'total_students': Student.objects.count(),
            'total_courses': Course.objects.count(),
        }
    else:
        messages.warning(request, "Complete your profile setup")
        return redirect('profile_setup')
        
    return render(request, 'accounts/dashboard.html', context)

def calculate_cgpa(enrollments):
    grade_points = {
        'A': 5.0,
        'B': 4.0,
        'C': 3.0,
        'D': 2.0,
        'E': 1.0,
        'F': 0.0
    }
    result = enrollments.filter(result__isnull=False).aggregate(
        total_points=Sum(
            Case(
                When(result__grade='A', then=5.0),
                When(result__grade='B', then=4.0),
                When(result__grade='C', then=3.0),
                When(result__grade='D', then=2.0),
                When(result__grade='E', then=1.0),
                default=0.0,
                output_field=FloatField()
            ) * F('course__credit_hours')
        ),
        total_credits=Sum('course__credit_hours')
    )
    return round(result['total_points'] / result['total_credits'], 2) if result['total_credits'] else 0.0

@login_required
def profile_setup(request):
    try:
        student = request.user.student
    except Student.DoesNotExist:
        student = None

    if request.method == 'POST':
        form = ProfileSetupForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('dashboard')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ProfileSetupForm(instance=student)

    return render(request, 'accounts/profile_setup.html', {
        'form': form,
        'user': request.user,
        'student': student,
    })