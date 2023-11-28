from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class CreateEvent(models.Model):
    eventUser = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='user')
    eventOwnerName = models.CharField(max_length= 25, blank=False, unique=True)
    eventTitle = models.CharField(max_length= 200, blank=False)
    eventDate = models.DateField(blank= False)
    eventTime = models.TimeField(blank= False)
    totalSeat = models.IntegerField(blank= False)
    eventLocation = models.CharField(max_length= 250, blank= False)
    eventDescription = models.TextField(blank= False)
    eventCreatedDate = models.DateTimeField(auto_now_add= True)
    eventModifyDate = models.DateTimeField(auto_now= True)
    

    def __str__(self) -> str:
        return self.eventOwnerName
    
    
class EventRegistration(models.Model):
    event = models.ForeignKey(CreateEvent, on_delete=models.CASCADE, blank=True, related_name='event')
    firstName = models.CharField(max_length=25, blank=False)
    lastName = models.CharField(max_length= 25, blank=False)
    email = models.EmailField(max_length= 50, blank=False)
    phoneNumber = models.CharField(max_length=14, blank=False)
    totalPerson = models.IntegerField(blank=False)
    createDate = models.DateTimeField(auto_now_add= True)
    modifyDate = models.DateTimeField(auto_now= True)
    
       
    def __str__(self) -> str:
        return self.event.eventOwnerName