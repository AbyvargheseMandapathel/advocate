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
    time_slot = forms.ModelChoiceField(queryset=TimeSlot.objects.none())  # Use ModelChoiceField

    def __init__(self, *args, **kwargs):
        lawyer = kwargs.pop('lawyer', None)
        available_time_slots = kwargs.pop('available_time_slots', None)
        
        super().__init__(*args, **kwargs)

        if lawyer and available_time_slots:
            print("Available Time Slots:", available_time_slots)  # Debugging statement
            self.fields['time_slot'].queryset = available_time_slots


            
            
        
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


