from django.shortcuts import render, redirect, get_object_or_404
from event.forms import CreateEventForm, EventRegistrationForm
from event.models import CreateEvent, EventRegistration
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
# Create your views here.

def all_event(request):
    all_events = CreateEvent.objects.all()
    
    available_seats_dict = {} # empty dictionary 
  
    for event in all_events:
        guests = EventRegistration.objects.filter(event=event)
        total_person = sum(guest.totalPerson for guest in guests)
        total_seat = event.totalSeat

        if total_person <= total_seat:
            available_seat = total_seat - total_person
        else:
            available_seat = 0  

        available_seats_dict[event.id] = available_seat

        
    context = {
        'all_events': all_events,
        'available_seats_dict' : available_seats_dict,
    }   
    return render(request, 'show_all_event.html', context)



def create_event(request):
    form = CreateEventForm()
    if request.method == 'POST':
        form = CreateEventForm(request.POST)
        if form.is_valid():
            form.instance.eventUser = request.user # eventUser is current user
            form.save()
            return redirect('home')
    else:
        form = CreateEventForm()
    return render(request, 'create_event.html', {'forms': form})



def event_registration(request, id=None):
    event = get_object_or_404(CreateEvent, id=id)

    form = EventRegistrationForm()
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            form.instance.event = event # instance of current event
            form.instance.eventUser = request.user # instance of current user
            form.save()
            return redirect('event_details', event.id)
    
    return render(request, 'event_registration.html', {'forms': form})


def event_details(request, id=None):
    event = get_object_or_404(CreateEvent, id=id)
    guests = EventRegistration.objects.filter(event= event)
    
    total_person = sum(guest.totalPerson for guest in guests)   
    # print(total_person)
    total_seat = event.totalSeat
    # totalGuest = len(guest)

    if total_person <= total_seat:
        avaiable_seat = total_seat - total_person

     
    context =  {
        
        'event': event, 
        'guests': guests,
        'avaiable_seat' : avaiable_seat,
        
        }

    return render(request, 'event_details.html', context)


def guest_details(request, id=None):
    guest = EventRegistration.objects.get(id= id)
    return render(request, 'guest_details.html', {'guest': guest})



def update_event(request, id=None):
    event = get_object_or_404(CreateEvent, id=id)
    
    if request.method == 'POST':
        form = CreateEventForm(request.POST, instance=event)
        if form.is_valid():
            input_date = form.cleaned_data['eventDate']
            input_time = form.cleaned_data['eventTime']
            current_date = timezone.now().date()
            current_time = timezone.localtime(timezone.now()).time()

            if input_date and input_date < current_date:
                messages.error(request, 'Invalid Date! Date must be in the future')
            elif input_time:               
                if not (9 <= input_time.hour <= 17):
                    messages.error(request, 'Event must be between 9 am and 5 pm')
                elif input_date == current_date and input_time <= current_time:
                    messages.error(request, 'Invalid Time! Time must be in the future')
                else:
                    form.save()
                    messages.success(request, 'Event updated successfully')
                    return redirect('event_details', event.id)
            else:
                form.save()
                messages.success(request, 'Event updated successfully')
                return redirect('event_details', event.id)
    else:
        form = CreateEventForm(instance=event)

    return render(request, 'update_event.html', {'form': form, 'event': event})


def delete_event(request, id=None):
    event = get_object_or_404(CreateEvent, id=id)

    if request.user != event.eventUser:
        return HttpResponse('Unathorized user')

    if request.method == 'POST':
        event.delete()
        return redirect('home')

    return render(request, 'delete_event.html', {'event': event})


def delete_guest(request, id=None):
    guest = get_object_or_404(EventRegistration, id=id)

    if request.user != guest.event.eventUser:
        return HttpResponse('unauthorized access')

    if request.method == 'POST':
        guest.delete()
        return redirect('event_details', guest.id)

    return render(request, 'delete_guest.html', {'guest': guest})
    