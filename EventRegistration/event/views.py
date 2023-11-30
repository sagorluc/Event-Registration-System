from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from event.forms import CreateEventForm, EventRegistrationForm
from event.models import CreateEvent, EventRegistration
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required
# Create your views here.

# ============================= SHOW ALL EVENT ==================================
@login_required
def all_event(request):
   all_events = CreateEvent.objects.all()
   
   event_data = []
   for event in all_events:
        guests = EventRegistration.objects.filter(event=event)
        total_person = sum(guest.totalPerson for guest in guests)
        available_seat = event.totalSeat - total_person

        event_data.append({
            'event': event,
            'available_seat': available_seat,
        })
   # print(event_data)

   context = {
        'all_events': event_data,
    }

   return render(request, 'show_all_event.html', context)

# ============================= CREATE EVENT ==================================
@login_required
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

# ============================= EVENT REGISTRATION ==============================
@login_required
def event_registration(request, id):
    event = CreateEvent.objects.get(pk=id)
    user = request.user
    
    # not allow to registration more then one event
    is_registered = EventRegistration.objects.filter(userE=request.user, event=event).first()
    if is_registered:
        return render(request, 'error_page.html', {'event': event})
   
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            
            # check if the user put more then the available seat 
            input_seat = form.cleaned_data['totalPerson']
            guests = EventRegistration.objects.filter(event= event)  
            total_person = sum(guest.totalPerson for guest in guests)   
            total_seat = event.totalSeat           
            if total_person <= total_seat:
                available_seat = total_seat - total_person               
                if input_seat > available_seat:
                    return render(request, 'not_seat_available.html')
            
            registration = form.save(commit=False) # not saveing immediately bcz of want to to manipulate the data
            registration.userE = user  # current user put in the event registration user
            registration.event = event # event put under evet registration 
            registration.save()
            return redirect('event_details', event.id)
    else:
        form = EventRegistrationForm()

    return render(request, 'event_registration.html', {'event': event, 'forms': form})


# ============================= EVENT DETAILS ==================================
@login_required
def event_details(request, id=None):
    event = get_object_or_404(CreateEvent, id=id)
    guests = EventRegistration.objects.filter(event= event)
    
    total_person = sum(guest.totalPerson for guest in guests)   
    # print(total_person)
    total_seat = event.totalSeat
    # totalGuest = len(guest)

    if total_person <= total_seat:
        available_seat = total_seat - total_person
            
    context =  {
        
        'event': event, 
        'guests': guests,
        'available_seat' : available_seat,
        
        }
        
    return render(request, 'event_details.html', context)



# ============================= GUEST DETAILS ==================================
@login_required
def guest_details(request, id=None):
    guest = EventRegistration.objects.get(id= id)
    return render(request, 'guest_details.html', {'guest': guest})


# ============================= UPDATE DETAILS ==================================
@login_required
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


# ============================= UPDATE GUEST ==================================
@login_required
def update_guest(request, id=None):
    guest = get_object_or_404(EventRegistration, id=id)
    
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST, instance = guest)
        if form.is_valid():
            input_person = form.cleaned_data['totalPerson']
            
            if input_person > 2:
               messages.error(request, 'Person should not be more the 2.')
            form.save()
            return redirect('guest_details', guest.id)
    else:
        form = EventRegistrationForm(instance = guest)
    return render(request, 'update_guest.html', {'form': form}) 
                
                
# ============================= DELETE EVENT ==================================
@login_required
def delete_event(request, id=None):
    event = get_object_or_404(CreateEvent, id=id)

    if request.user != event.eventUser:
        return HttpResponse('Unathorized user')

    if request.method == 'POST':
        event.delete()
        return redirect('dashboard')

    return render(request, 'delete_event.html', {'event': event})


# ============================= DELETE GUEST ==================================
@login_required
def delete_guest(request, id):
    guest = get_object_or_404(EventRegistration, id=id)

    if request.method == 'POST':
        guest.delete()
        return redirect('dashboard')

    return render(request, 'delete_guest.html', {'guest': guest})
    

# ============================= DASHBOARD ==================================   
@login_required   
def dashboard(request):
    events = CreateEvent.objects.filter(eventUser= request.user)  
    guests = EventRegistration.objects.filter(userE= request.user)
     
    context = {
        'events' : events,
        'guests' : guests,
    }   
    return render(request, 'dashboard.html', context)


# ========================== SEARCH EVENT AND GUEST ===============================
@login_required
def search_guest_event(request):
    input_query = request.GET.get('keyword')
    
    events = CreateEvent.objects.all()
    guests = EventRegistration.objects.all()
    
    # number base searching
    try:
        id_query = int(input_query)
        events = events.filter(id=id_query)
    except ValueError:
        pass  
    
    
    events = events.filter(
        Q(eventTitle__icontains=input_query) |
        Q(eventUser__username__icontains=input_query) |
        Q(eventOwnerName__icontains=input_query) |
        Q(eventDate__icontains=input_query) |
        Q(eventLocation__icontains=input_query)
    )
    
    
    guests = guests.filter(
        Q(firstName__icontains=input_query) |
        Q(lastName__icontains=input_query) |
        Q(email__icontains=input_query)
    )
    
    # date-based filtering
    try:
        date_input = timezone.datetime.strptime(input_query, '%Y-%m-%d').date()
        events = events.filter(eventDate=date_input)
        guests = guests.filter(createDate=date_input)
    except ValueError:
        pass

    
    if events:
        context = {'events' : events, }
        return render(request, 'search_guest_event.html', context)
    else:
        context = {'guests' : guests}
        return render(request, 'search_guest_event.html', context)
    
    

# =========================== FILTER EVENT AND GUEST ===============================       
@login_required
def filter_event(request):
    input_event_date = request.GET.get('eventDate')
    input_event_location = request.GET.get('location')
    
    events = CreateEvent.objects.filter(eventUser= request.user)
    guests = EventRegistration.objects.filter(userE= request.user)
    
    if input_event_date:
        events = events.filter(Q(eventDate=input_event_date))
        guests = guests.filter(Q(event__eventDate=input_event_date))
        
    if input_event_location:
        events = events.filter(Q(eventLocation__icontains= input_event_location))
        guests = guests.filter(Q(event__eventLocation__icontains=input_event_location))
        
    return render(request, 'dashboard.html', {'events' : events, 'guests' : guests})


# =========================== COMMON DATA =============================
# def get_common_data(event, guests):
#     total_person = sum(guest.totalPerson for guest in guests)
#     total_seat = event.totalSeat

#     common_data = {
#         'event': event,
#         'guests': guests,
#     }

#     if total_person <= total_seat:
#         common_data['available_seat'] = total_seat - total_person

#     return common_data