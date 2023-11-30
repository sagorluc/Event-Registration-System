from typing import Any
from django import forms
from event.models import CreateEvent, EventRegistration
from django.utils import timezone

# ============================ CREATE EVENT FORM ====================================
class CreateEventForm(forms.ModelForm):
    class  Meta:
        model = CreateEvent
        fields = ['eventOwnerName', 'eventTitle', 'eventDate', 'eventTime', 'totalSeat', 'eventLocation', 'eventDescription']
        
        
        labels = {
            'eventOwnerName': 'Event Creator Name',
            'eventTitle': 'Event Title',
            'eventDate': 'Event Date',
            'eventTime': 'Event Time',
            'totalSeat': 'Total Seats',
            'eventLocation': 'Event Location',
            'eventDescription': 'Event Description',
        }
        
        # set format of calender and time
        widgets = {
            'eventDate': forms.DateInput(attrs={'type': 'date'}),
            'eventTime': forms.TimeInput(attrs={'type': 'time'}),
        }
        
    # set place holder by overriding    
    def __init__(self, *args, **kwargs):
        super(CreateEventForm, self).__init__(*args, **kwargs)
        self.fields['eventOwnerName'].widget.attrs['placeholder'] = 'Enter academic name'
        self.fields['eventTitle'].widget.attrs['placeholder'] = 'Enter the event title'
        self.fields['eventDate'].widget.attrs['placeholder'] = 'Select the event date'
        self.fields['eventTime'].widget.attrs['placeholder'] = 'Select the event time'
        self.fields['totalSeat'].widget.attrs['placeholder'] = 'Enter total number of seats'
        self.fields['eventLocation'].widget.attrs['placeholder'] = 'Enter the event location'
        self.fields['eventDescription'].widget.attrs['placeholder'] = 'Enter a brief description of the event'
        
    def clean(self):
        cleaned_data = super().clean()
        input_date = cleaned_data.get('eventDate')
        input_time = cleaned_data.get('eventTime')
        current_date = timezone.now().date()
        
        if input_date and input_date < current_date:
            raise forms.ValidationError('Invalid Date! Date must be in future')

        if input_time:
            current_time = timezone.localtime(timezone.now()).time()
            if not (9 <= input_time.hour <= 17):
                raise forms.ValidationError('Event must be 9am and 5pm')
            elif input_date == timezone.now().date() and input_time <= current_time:
                raise forms.ValidationError('Invalid Time! Time must be in future')

    
    def clean_totalSeat(self):
        input_seat = self.cleaned_data['totalSeat']
        
        if input_seat > 50:
            raise forms.ValidationError("Total seat can not be take more the 50.")
        elif input_seat < 0:
            raise forms.ValidationError('The seat can not be negative!')
        
        return input_seat

# ======================== EVENT REGISTRATION FORM =================================
class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['firstName', 'lastName', 'email', 'phoneNumber', 'totalPerson']
        
        
        labels = {
            'firstName': 'First name',
            'lastName': 'Last name',
            'email': 'Email',
            'phoneNumber': 'Mobile number',
            'totalPerson': 'Person',

        }
    # set placeholder by overriding   
    def __init__(self, *args, **kwargs):
        super(EventRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['firstName'].widget.attrs['placeholder'] = 'Enter your first name'
        self.fields['lastName'].widget.attrs['placeholder'] = 'Enter your last name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'
        self.fields['phoneNumber'].widget.attrs['placeholder'] = 'Enter your mobile number'
        self.fields['totalPerson'].widget.attrs['placeholder'] = 'How many person you are?'

    def clean_totalPerson(self):
        input_person = self.cleaned_data['totalPerson']
        
        if input_person > 2:
            raise forms.ValidationError('The person should not be more then 2.')
        
        return input_person