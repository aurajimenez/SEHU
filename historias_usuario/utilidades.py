
# Decorador que verifica que el usuario tenga alguno de los cargos permitidos
from django.contrib import messages
from django.shortcuts import redirect
from datetimewidget.widgets import DateWidget
from datetimewidget.widgets import DateTimeWidget
from datetimewidget.widgets import TimeWidget

def verificar_cargo(cargos_permitidos):
    def _method_wrapper(view_method):
        def _arguments_wrapper(request, *args, **kwargs):
            request_inicial = request
            if hasattr(request, "request"):
                request = request.request

            try:
                usuario = request.user
                if not (usuario.cargo in cargos_permitidos):
                    messages.error(request, "Usted no tiene ninguno de los cargos permitidos para acceder a la página solicitada")
                    return redirect('inicio')
            except AttributeError:
                messages.error(request, "Para acceder a la página solicitada requiere loguearse")
                return redirect('login')

            return view_method(request_inicial, *args, **kwargs)
        return _arguments_wrapper
    return _method_wrapper

# Funcion que me retorna el selector de fecha
def MyDateWidget():
    return DateWidget(usel10n=False, bootstrap_version=3, options={'format': 'yyyy-mm-dd', 'startView':4, 'pickerPosition': 'bottom-left','language':'es'})

# Funcion que me retorna el selector de fecha y hora
def MyDateTimeWidget():
    return DateTimeWidget(usel10n=False, bootstrap_version=3, options={'format': 'yyyy-mm-dd hh:ii', 'startView':4, 'language':'es'})

# Función que retorna el selector de hora
def MyTimeWidget():
    return TimeWidget(usel10n=False, bootstrap_version=3, options={'format': 'hh:ii', 'startView':1, 'language':'es'})   


