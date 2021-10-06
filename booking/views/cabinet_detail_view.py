from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.views.generic import CreateView
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from booking.models import Cabinet, Event
from booking.forms import EventForm
from booking.services import create_schedule


class CabinetDetailView(LoginRequiredMixin, CreateView):
    form_class = EventForm
    template_name = 'cabinets/cabinets_detail.html'

    def get_object(self, *args, **kwargs):
        try:
            return Cabinet.objects.get(room_number=self.kwargs.get('pk'))
        except Cabinet.DoesNotExist:
            raise Http404

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = Event.room_objects.filter(cabinet__room_number=self.kwargs.get('pk')).values()
        context['schedule'] = create_schedule(event)
        context['cabinet'] = self.get_object()
        return context

    def form_valid(self, form):
        new_event = form.save(commit=False)
        new_event.owner = self.request.user
        new_event.cabinet = self.get_object()
        new_event.save()

        return render(self.request, 'cabinets/cabinets_detail.html')
