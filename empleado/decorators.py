from functools import wraps
from django.shortcuts import redirect
from .models import Empleado

def empleado_login_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        empleado_id = request.session.get('empleado_id')

        if not empleado_id:
            return redirect('ingreso_empleado')

        try:
            empleado = Empleado.objects.get(pk=empleado_id)
        except Empleado.DoesNotExist:
            request.session.pop('empleado_id', None)
            return redirect('ingreso_empleado')

        request.empleado = empleado
        return view_func(request, *args, **kwargs)
    return _wrapped
