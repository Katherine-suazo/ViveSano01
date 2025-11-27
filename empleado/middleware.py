from django.shortcuts import redirect
from .models import Empleado


class EmpleadoLoginRequiredMiddleware:
    """Middleware que exige que exista `empleado_id` en la sesión para acceder a la mayoría de rutas.

    - Carga `request.empleado` cuando `empleado_id` está presente en la sesión.
    - Redirige a `/` (login) si no hay sesión y la ruta no está en la allowlist.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # Allowlisted prefixes and exact paths
        allow_prefixes = ['/admin/', '/static/', '/media/', '/favicon.ico']
        allow_exact = ['/', '/registro_empleado/', '/ingreso_empleado/']

        # If there's an empleado_id in session, try to load the Empleado
        empleado_id = request.session.get('empleado_id')
        if empleado_id:
            try:
                request.empleado = Empleado.objects.get(pk=empleado_id)
            except Empleado.DoesNotExist:
                request.empleado = None
        else:
            request.empleado = None

        # Allow requests to public paths
        if any(path.startswith(pref) for pref in allow_prefixes) or path in allow_exact:
            return self.get_response(request)

        # If no empleado in session, redirect to login
        if not request.empleado:
            return redirect('/')

        return self.get_response(request)
