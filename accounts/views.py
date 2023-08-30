# accounts/views.py
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import CustomUser, LawyerProfile  # Import LawyerProfile model
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
from django.core.exceptions import ValidationError
from datetime import datetime

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']  # Change this to 'email'
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)  # Use email for authentication
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
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        adharno = request.POST['adharno']
        address = request.POST['address']
        dob = request.POST['dob']
        pin = request.POST['pin']
        state = request.POST['state']
        phone = request.POST['phone']
        user_type = request.POST['user_type']

        
        # Check if the email is already in use
        if CustomUser.objects.filter(email=email).exists():
            # You can customize this error message as needed
            raise ValidationError('This email is already in use.')

        # Check if the user creating the account is a superuser
        # if request.user.is_superuser:
        #     user_type = 'admin'
        # else:
        #     user_type = request.POST['user_type']

        # Create the user with the determined user_type and email as username
        user = CustomUser.objects.create_user(
            email=email,
            username=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            adharno=adharno,
            address=address,
            dob=dob,
            pin=pin,
            state=state,
            phone=phone,
            user_type=user_type,
        )
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
        # username = request.POST['username']
        email = request.POST['email']
        # Save additional fields to LawyerProfile model
        specialization = request.POST['specialization']
        # start_date = request.POST['start_date']
        start_date_str = request.POST['start_date']
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        # experience = request.POST['experience']
        profile_picture = request.FILES.get('profile_picture')
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        adharno = request.POST['adharno']
        address = request.POST['address']
        dob = request.POST['dob']
        pin = request.POST['pin']
        state = request.POST['state']
        phone = request.POST['phone']

        # Create a new user with user_type 'lawyer'
        user = CustomUser.objects.create_user(
            username=email, 
            email=email, 
            user_type='lawyer',
            first_name = first_name,
            last_name = last_name,
            adharno = adharno,
            address = address,
            dob = dob,
            pin = pin,
            state = state,
            phone   = phone,    
            )

        

        lawyer_profile = LawyerProfile.objects.create(
            user=user,
            specialization=specialization,
            start_date=start_date,  # Use the converted start_date here
            # experience=experience,
            profile_picture=profile_picture
        )

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

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')