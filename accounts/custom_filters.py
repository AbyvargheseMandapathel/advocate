# custom_filters.py
from django import template
from .models import TimeSlot  # Replace 'your_app' with the actual name of your app

register = template.Library()

@register.filter
def is_in_lawyer_working_hours(slot, lawyer_working_hours):
    day, slot_value = slot.split('|')
    return (day, slot_value) in lawyer_working_hours
