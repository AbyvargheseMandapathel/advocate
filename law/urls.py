# law/urls.py
from django.contrib import admin
from django.urls import path, include 
from accounts import views# Import the include function
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('lawyerlist/', views.lawyer_list, name='lawyer_list'),
    path('about/', views.about, name='about'),
    path('practice/', views.practice, name='practice'),
    path('contact/', views.contact, name='contact'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')), 
    path('accounts/', include('allauth.urls')),
    path('error/', views.error, name='error'),
    path('book/', views.book, name='book'),
    path('submit/', views.submit, name='submit'),
    # path('book_lawyer/<int:lawyer_id>/', views.book_lawyer, name='book_lawyer'),
    path('book_lawyer/<int:lawyer_id>/', views.book_lawyer, name='book_lawyer'),
    path('booking/<int:booking_id>/', views.booking_details, name='booking_details'),
    path('internship/<int:internship_id>/', views.internship_detail, name='internship_detail'),
    path('mark_holiday/', views.mark_holiday, name='mark_holiday'),
    path('reschedule/<int:booking_id>/', views.reschedule_appointment, name='reschedule_appointment'),
    path('bookings/', views.all_bookings, name='all_bookings'),
    path('lawyers_list/', views.list_lawyers, name='list_lawyers'),
    path('admin_view_holiday_requests/', views.admin_view_holiday_requests, name='admin_view_holiday_requests'),
    path('admin_approve_reject_holiday/<int:request_id>/', views.admin_approve_reject_holiday, name='admin_approve_reject_holiday'),
    path('enter_client_email/', views.enter_client_email, name='enter_client_email'),
    path('enter_case_details/<int:client_id>/<int:lawyer_id>/', views.enter_case_details, name='enter_case_details'),
    path('case_detail/<int:case_id>/', views.case_detail, name='case_detail'),
    path('current_cases/', views.current_cases, name='current_cases'),
    path('list_cases/', views.list_cases, name='list_cases'),
    path('set_working_hours/', views.set_working_hours, name='set_working_hours'),
    path('update_working_hours/', views.update_working_hours, name='update_working_hours'),
    path('get_available_time_slots/', views.get_available_time_slots, name='get_available_time_slots'),
    # path('update_booking_status/', views.update_booking_status, name='update_booking_status'),


    # path('get_time_slots/', views.get_time_slots, name='get_time_slots'),

    # path('students/internship/<str:lawyer_name>/', views.internship_detail, name='internship_detail')


    
    

    # path('lawyer/<int:lawyer_id>/', views.lawyer_details, name='lawyer_details'),

    # Add other URL patterns for your project
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
