from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import CreateView

from booking.forms import BookingForm
from booking.models import Event
from booking.services import create_schedule


class BookingView(LoginRequiredMixin, CreateView):
    form_class = BookingForm
    template_name = 'cabinets/cabinets_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event = Event.room_objects.filter(cabinet__room_number=self.kwargs.get('pk')).values()
        context['schedule'] = create_schedule(event)
        return context

    def form_invalid(self, form):
        return JsonResponse({'errors': str(form.non_field_errors())}, status=400)

    def form_valid(self, form):
        new_event = form.save(commit=False)
        new_event.owner = self.request.user
        new_event.save()
        return JsonResponse({}, status=200)


