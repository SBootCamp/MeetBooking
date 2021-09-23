from django.http import Http404
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView

from .models import *
from .services import create_update_date,schedule


# class BookingView(CreateView):
#     form_class = BookingForm


class BookingView(View):
    def get(self, request, *args, **kwargs):

        schedule(kwargs.get('pk'))
        # try:
        #     schedule = ScheduleBooking.objects.filter(cabinet__room_number=kwargs.get('pk')).values()
        #     print(schedule)
        # except Event.DoesNotExist:
        #     raise Http404
        context = {

        }
        return render(request, 'cabinet/form_booking.html', context)
