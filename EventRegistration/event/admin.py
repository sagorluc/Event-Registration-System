from django.contrib import admin
from event.models import CreateEvent, EventRegistration
# Register your models here.

class CreateEventAdmin(admin.ModelAdmin):
    list_display = ['id', 'eventOwnerName', 'eventTitle', 'eventDate', 'eventTime', 'totalSeat']
    ordering = ['id']
    
    class Meta:
        verbose_name = 'CreateEvent'
        verbose_name_plural = 'CreateEvents'
        
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['id', 'event', 'firstName', 'email', 'phoneNumber', 'totalPerson']
    ordering = ['id']
    
    class Meta:
        verbose_name = 'EventRegistration'
        verbose_name_plural = 'EventRegistrations'
        
        
admin.site.register(CreateEvent, CreateEventAdmin)
admin.site.register(EventRegistration, EventRegistrationAdmin)