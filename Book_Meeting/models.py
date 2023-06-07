from django.db import models
from Accounts.models import Status
from datetime import date, timezone


class Room(models.Model):
    Room_Name = models.CharField(max_length=150)
    
    def __str__(self):
        return self.Room_Name

    class Meta:
        verbose_name_plural = 'Rooms'
        
class TimeSlot(models.Model):
    Time = models.CharField(max_length=150)
    
    def __str__(self):
        return self.Time
    
    class Meta:
        verbose_name_plural = 'Time Slots'
        
class BookedRoom(models.Model):
    Room = models.ForeignKey(Room, on_delete=models.CASCADE, default=None)
    Booked_By = models.EmailField()
    Date = models.DateField(default=date.today)
    Time_From = models.TimeField()
    Time_End = models.TimeField()
    Time = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, default=1)
    Status = models.ForeignKey(Status, on_delete=models.CASCADE, default=1)
    
