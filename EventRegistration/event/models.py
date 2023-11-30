from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

# ============================ CREATE EVENT MODEL ====================================
class CreateEvent(models.Model):
    eventUser        = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='user')
    eventOwnerName   = models.CharField(max_length= 25, blank=False, unique=True)
    eventTitle       = models.CharField(max_length= 200, blank=False)
    eventDate        = models.DateField(blank= False)
    eventTime        = models.TimeField(blank= False)
    totalSeat        = models.IntegerField(blank= False)
    eventLocation    = models.CharField(max_length= 250, blank= False)
    eventDescription = models.TextField(blank= False)
    eventCreatedDate = models.DateTimeField(auto_now_add= True)
    eventModifyDate  = models.DateTimeField(auto_now= True)
    
    class Meta:
        verbose_name = 'Create Event'
        verbose_name_plural = 'Create Events'
        ordering = ['id']
    

    def __str__(self) -> str:
        return str(self.eventUser)
    
# ======================== EVENT REGISTRATION MODEL ===============================   
class EventRegistration(models.Model):
    userE       = models.ForeignKey(User, on_delete=models.CASCADE, default=False, related_name='registration')
    event       = models.ForeignKey(CreateEvent, on_delete=models.CASCADE, blank=True, related_name='event')
    firstName   = models.CharField(max_length=25, blank=False)
    lastName    = models.CharField(max_length= 25, blank=False)
    email       = models.EmailField(max_length= 50, blank=False)
    phoneNumber = models.CharField(max_length=14, blank=False)
    totalPerson = models.IntegerField(blank=False)
    createDate  = models.DateTimeField(auto_now_add= True)
    modifyDate  = models.DateTimeField(auto_now= True)
    
    class Meta:
        verbose_name = 'Event Registration'
        verbose_name_plural = 'Event Registrations'
        ordering = ['id']
    
       
    def __str__(self) -> str:
        return str(self.event)
