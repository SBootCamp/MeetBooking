from django import forms

from booking.models import Event


class BookingForm(forms.ModelForm):
    class Meta:
        model = Event