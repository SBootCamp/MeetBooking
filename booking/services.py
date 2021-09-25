from .models import Event
from .forms import TIMES,DATES


def create_schedule(room_number):
    event = Event.objects.filter(cabinet__room_number=room_number)
    schedule = {}


