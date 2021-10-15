from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.db import IntegrityError

from booking.models import Cabinet, Event
from booking.forms import EventForm
from booking.services import create_schedule


class CabinetDetailView(LoginRequiredMixin, CreateView):
    form_class = EventForm
    template_name = 'cabinets/cabinets_detail.html'

    def get_object(self, *args, **kwargs):
        return get_object_or_404(Cabinet, name=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        events = Event.room_objects.filter(cabinet__name=self.kwargs.get('pk')).values()
        schedule = Paginator(create_schedule(events), 7)
        context['schedule'] = schedule
        context['cabinet'] = self.get_object()
        return context

    def form_valid(self, form):
        new_event = form.save(commit=False)
        new_event.owner = self.request.user
        new_event.cabinet = self.get_object()
        try:
            new_event.save()
            form.save_m2m()
        except IntegrityError as exp:
            if 'check_datetime' in str(exp):
                form.add_error(None, 'Время окончания мероприятия должно быть больше начала')
            else:
                form.add_error(None, 'Указанное время занято')
            return render(self.request, 'cabinets/cabinets_detail.html', self.get_context_data(form=form))
        return render(self.request, 'cabinets/cabinets_detail.html', self.get_context_data())
