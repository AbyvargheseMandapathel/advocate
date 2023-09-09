from django import forms
from django.contrib.auth.forms import SetPasswordForm
from .models import Booking ,Internship ,LawyerProfile, TimeSlot

class CustomPasswordResetForm(SetPasswordForm):
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput,
        help_text="Enter the same password as above, for verification."
    )
    
    
# class LoginForm(forms.Form):
#     email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    
class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['details', 'booking_date', 'time_slot']

    booking_date = forms.DateField(widget=forms.SelectDateWidget)
    time_slot = forms.ChoiceField(choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Get the lawyer associated with this booking, if available
        lawyer = self.initial.get('lawyer')
        
        if lawyer:
            # Debugging: Print lawyer's working hours to check the values
            print(f"Lawyer Working Hours - Start: {lawyer.working_time_start}, End: {lawyer.working_time_end}")
            
            # Filter time slots based on lawyer's working hours
            available_time_slots = TimeSlot.objects.filter(
                start_time__gte=lawyer.working_time_start,
                end_time__lte=lawyer.working_time_end
            )
            
            # Debugging: Print the available time slots to check if they are filtered correctly
            print("Available Time Slots:")
            for ts in available_time_slots:
                print(f"{ts.start_time} - {ts.end_time}")
            
            # Create choices for the time slot field
            time_slot_choices = [(ts.pk, f'{ts.start_time} - {ts.end_time}') for ts in available_time_slots]
            self.fields['time_slot'].choices = time_slot_choices
            
            
        
class InternshipForm(forms.ModelForm):
    class Meta:
        model = Internship
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter lawyers with experience 5 or more years
        self.fields['lawyer_profile'].queryset = LawyerProfile.objects.filter(experience__gte=5)
        
        # Use DateInput widget for the start_date field
        self.fields['start_date'].widget = forms.DateInput(attrs={'type': 'date'})  # Set the input type to 'date'


