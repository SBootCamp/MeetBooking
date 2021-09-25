from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView

from .models import Event, Cabinet

from .forms import BookingForm


class CabinetListView(ListView):
    queryset = Cabinet.objects.all()
    template_name = 'cabinet/list_cabinets.html'


class BookingView(LoginRequiredMixin, CreateView):
    form_class = BookingForm
    template_name = 'cabinet/form_booking.html'
    success_url = 'booking'

    def get_queryset(self, *args, **kwargs):
        return Event.objects.filter(cabinet__room_number=self.kwargs.get('pk'))


    def form_valid(self, form):
        new_event = form.save(commit=False)
        new_event.owner = self.request.user
        new_event.save()
        return HttpResponseRedirect(reverse('cabinet_list'))
