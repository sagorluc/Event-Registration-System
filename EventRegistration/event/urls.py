from django.urls import path
from event.views import all_event, create_event, event_registration, \
    event_details, guest_details, update_event, delete_event, delete_guest

urlpatterns = [
    path('', all_event, name="home"),
    path('create_event/', create_event, name="create_event"),
    path('event_register/<int:id>/', event_registration, name="event_register"),
    path('event_details/<int:id>/', event_details, name="event_details"),
    path('guest_details/<int:id>/', guest_details, name="guest_details"),
    path('update_event/<int:id>/', update_event, name="update_event"),
    path('delete_event/<int:id>/', delete_event, name="delete_event"),
    path('delete_guest/<int:id>/', delete_guest, name="delete_guest"),
]
