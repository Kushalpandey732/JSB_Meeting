from .models import Room,BookedRoom, TimeSlot
from django.contrib import admin

admin.site.register(Room)
admin.site.register(BookedRoom)
admin.site.register(TimeSlot)