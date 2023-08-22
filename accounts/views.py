# accounts/views.py
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import CustomUser
from django.http import HttpResponseForbidden
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
# from django.contrib.auth.forms import SetPasswordForm
from .forms import CustomPasswordResetForm  # Import your custom form class



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
    
def add_lawyer(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("Access Denied")

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        user = CustomUser.objects.create_user(username=username, user_type='lawyer')
        
        # Generate a unique token for password reset
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(request)
        protocol = 'http'  # Change to 'https' if using HTTPS
        password_reset_url = f"{protocol}://{current_site.domain}/accounts/set/{uid}/{token}/"

        # Render the email body template
        message = render_to_string(
            'registration/password_set_email.html',
            {
                'user': user,
                'password_reset_url': password_reset_url,
            }
        )

        # Send the email with custom template
        send_mail(
            'Set Your Password',
            '',
            'noreply@example.com',  # Sender's email address
            [email],
            fail_silently=False,
            html_message=message  # Use the custom HTML template
        )

        return redirect('admin_dashboard')  # Redirect back to admin dashboard
    
    return render(request, 'admin/add_lawyer.html')

# def custom_password_set_confirm(request, uidb64, token):
#     user_id = urlsafe_base64_decode(uidb64)
#     user = CustomUser.objects.get(pk=user_id)
    
#     if request.method == 'POST':
#         form = SetPasswordForm(user, request.POST)
#         if form.is_valid():
#             form.save()
#             # Log the user in after setting the password
#             user = authenticate(username=user.username, password=form.cleaned_data['new_password1'])
#             login(request, user)
#             return redirect('dashboard')  # Redirect to the dashboard or another page
#     else:
#         form = SetPasswordForm(user)
    
#     return render(request, 'registration/password_set_confirm.html', {'form': form, 'user': user})


def custom_password_set_confirm(request, uidb64, token):
    user_id = urlsafe_base64_decode(uidb64)
    user = CustomUser.objects.get(pk=user_id)
    
    if request.method == 'POST':
        form = CustomPasswordResetForm(user, request.POST)
        if form.is_valid():
            form.save()
            # Log the user in after setting the password
            user = authenticate(username=user.username, password=form.cleaned_data['new_password1'])
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard or another page
    else:
        form = CustomPasswordResetForm(user)
    
    return render(request, 'registration/password_set_confirm.html', {'form': form, 'user': user})