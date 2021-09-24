from django.http import Http404
from django.shortcuts import render
from django.views import View
from django.views.generic import CreateView

from .models import *
from .services import *


# class BookingView(CreateView):
#     form_class = BookingForm


# class BookingView(CreateView):
#
#         return render(request, 'cabinet/form_booking.html')
