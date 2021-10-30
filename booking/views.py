import datetime

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.db import IntegrityError, transaction

from booking.models import Cabinet, Event
from booking.forms import EventForm
from booking.services import create_schedule, create_datetime_list


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
        period_duplication = datetime.timedelta(days=settings.PERIOD_DUPLICATION_DAYS)
        data = form.cleaned_data
        duplication = data.pop('duplication')
        try:
            with transaction.atomic():
                new_event.save()
                form.save_m2m()
                if duplication:
                    visitors = data.pop('visitors')
                    while data['start_time'] + period_duplication in create_datetime_list():
                        data['start_time'] += period_duplication
                        data['end_time'] += period_duplication
                        event = Event.objects.create(**data, cabinet=self.get_object(), owner=self.request.user)
                        event.visitors.add(*visitors)
        except IntegrityError as exp:
            if 'check_datetime' in str(exp):
                form.add_error(None, 'Время окончания мероприятия должно быть больше начала')
            elif 'overlap_booking' in str(exp) and not duplication:
                form.add_error(None, 'Указанное время занято')
            else:
                form.add_error(None, 'Невозможно продублировать мероприятие')
            return render(self.request, 'cabinets/cabinets_detail.html', self.get_context_data(form=form))
        return render(self.request, 'cabinets/cabinets_detail.html', self.get_context_data())
