from .models import Event



def create_schedule(room_number):
    event = Event.objects.filter(cabinet__room_number=room_number)
    schedule = {}


