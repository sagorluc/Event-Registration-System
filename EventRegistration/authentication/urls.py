from django.urls import path
from authentication.views import user_register, log_in, log_out

urlpatterns = [
    path('register/', user_register, name='register'),
    path('login/', log_in, name='login'),
    path('logout/', log_out, name='logout'),
]
