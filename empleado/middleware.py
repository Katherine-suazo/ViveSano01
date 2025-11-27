from django.shortcuts import redirect
from .models import Empleado


class EmpleadoLoginRequiredMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        allow_prefixes = ['/admin/', '/static/', '/media/', '/favicon.ico']
        allow_exact = ['/', '/registro_empleado/', '/ingreso_empleado/']

        empleado_id = request.session.get('empleado_id')
        if empleado_id:
            try:
                request.empleado = Empleado.objects.get(pk=empleado_id)
            except Empleado.DoesNotExist:
                request.empleado = None
        else:
            request.empleado = None

        if any(path.startswith(pref) for pref in allow_prefixes) or path in allow_exact:
            return self.get_response(request)
        
        if not request.empleado:
            return redirect('/')

        return self.get_response(request)
