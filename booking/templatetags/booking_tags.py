from django import template
from booking.forms import BookingForm

register = template.Library()


@register.inclusion_tag("booking_tags/booking_form.html")
def booking_form():
    return {"form": BookingForm()}
