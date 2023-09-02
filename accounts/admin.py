from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, LawyerProfile , ContactEntry , Booking , Student, Internship

class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'user_type', 'adharno', 'address', 'dob', 'pin', 'state', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

# Register the CustomUser model with the updated admin class
admin.site.register(CustomUser, CustomUserAdmin)
@admin.register(LawyerProfile)
class LawyerProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'specialization', 'experience', 'start_date', 'profile_picture')
    
admin.site.register(ContactEntry)
admin.site.register(Booking)
admin.site.register(Student)
admin.site.register(Internship)


