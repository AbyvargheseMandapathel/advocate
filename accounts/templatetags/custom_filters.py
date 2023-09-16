from django import template
from accounts.models import TimeSlot  # Import your TimeSlot model

register = template.Library()

@register.filter(name='is_in_lawyer_working_hours')
def is_in_lawyer_working_hours(slot, lawyer):
    return lawyer.working_hours.filter(day=slot.day, slot=slot.slot).exists()
