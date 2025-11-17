from django.contrib import admin
from django.urls import path, include

urlpatterns = [

    path('', include('empleado.urls')),
    
    path('clientes/', include('cliente.urls')),

    path('productos/',include('producto.urls')),

    path('admin/', admin.site.urls),

]
