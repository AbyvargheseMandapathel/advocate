# accounts/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('client/dashboard/', views.client_dashboard, name='client_dashboard'),
    path('lawyer/dashboard/', views.lawyer_dashboard, name='lawyer_dashboard'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
    path('add_lawyer/', views.add_lawyer, name='add_lawyer'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('set/<uidb64>/<token>/', views.custom_password_set_confirm, name='password_reset_confirm'),
]
