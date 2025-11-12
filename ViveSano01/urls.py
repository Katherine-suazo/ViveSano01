from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('clientes/', include('cliente.urls')),

    path('admin/', admin.site.urls)

]
