from django.views.generic import ListView

from booking.models import Cabinet

class CabinetListView(ListView):
    queryset = Cabinet.objects.all()
    template_name = 'cabinets/cabinets_list.html'