# accounts/views.py
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import CustomUser
from django.http import HttpResponseForbidden


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.user_type == 'admin':
                return redirect(reverse('admin_dashboard'))
            elif user.user_type == 'client':
                return redirect(reverse('client_dashboard'))
            elif user.user_type == 'lawyer':
                return redirect(reverse('lawyer_dashboard'))
            elif user.user_type == 'student':
                return redirect(reverse('student_dashboard'))
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user_type = request.POST['user_type']
        user = CustomUser.objects.create_user(username=username, password=password, user_type=user_type)
        return redirect('login')
    return render(request, 'signup.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def dashboard_view(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html', {'user': request.user})
    else:
        return redirect('login')
    
    # accounts/views.py
def admin_dashboard(request):
    if request.user.user_type == 'admin':
        return render(request, 'admin/dashboard.html', {'user': request.user})
    else:
        return HttpResponseForbidden("Access Denied")

def student_dashboard(request):
    if request.user.user_type == 'student':
        return render(request, 'student/dashboard.html', {'user': request.user})
    else:
        return HttpResponseForbidden("Access Denied")

def client_dashboard(request):
    return render(request, 'client/dashboard.html', {'user': request.user})

def lawyer_dashboard(request):
    if request.user.user_type == 'lawyer':
        return render(request, 'lawyer/dashboard.html', {'user': request.user})
    else:
        return HttpResponseForbidden("Access Denied")





