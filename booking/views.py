from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, DetailView
from .models import Event, Cabinet
from .forms import BookingForm
from .services import create_schedule


class CabinetListView(ListView):
    queryset = Cabinet.objects.all()
    template_name = 'cabinet/list_cabinets.html'


class CabinetDetailView(DetailView):
    template_name = 'cabinet/detail_cabinet.html'

    def get_object(self, queryset=None):
        try:
            return Cabinet.objects.get(room_number=self.kwargs.get('pk'))
        except Cabinet.DoesNotExist:
            raise Http404


class BookingView(LoginRequiredMixin, CreateView):
    form_class = BookingForm
    success_url = 'booking'

    def form_valid(self, form):
        new_event = form.save(commit=False)
        new_event.owner = self.request.user
        new_event.save()
        return HttpResponseRedirect(reverse('cabinet_list'))
