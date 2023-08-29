# law/urls.py
from django.contrib import admin
from django.urls import path, include 
from accounts import views# Import the include function

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')), 
    path('accounts/', include('allauth.urls')),# Include the accounts app URLs
    # Add other URL patterns for your project
]
