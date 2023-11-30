
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('event/', include('event.urls')),
    path('accounts/', include('authentication.urls')),
    path('api/', include('API.urls'), name='api'),
]
