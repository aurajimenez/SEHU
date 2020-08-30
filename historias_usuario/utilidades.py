
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
            if hasattr(request, "request"):  # Es una CBV
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


# Funcion que me permite dejar solo la primera letra en mayuscula de ciertos campos de un formulario
# PARAMS:
# form_data = datos del formulario
# campos = listado de campos del formulario los cuales queremos convertir la primera letra en mayuscula
def capitalizar_texto_campos(form_data, campos):
    for campo in campos:
        form_data[campo] = form_data[campo].lower().capitalize()
    return form_data

# Funcion que me permite convertir a mayuscula ciertos campos de un formulario
# PARAMS:
# form_data = datos del formulario
# campos = listado de campos del formulario los cuales queremos convertir en mayuscula
def mayuscula_texto_campos(form_data, campos):
    for campo in campos:
        form_data[campo] = form_data[campo].upper()
    return form_data



# Funcion que me retorna el selector de fecha
def MyDateWidget():
    return DateWidget(usel10n=False, bootstrap_version=3, options={'format': 'yyyy-mm-dd', 'startView':4, 'pickerPosition': 'bottom-left','language':'es'})

# Funcion que me retorna el selector de fecha y hora
def MyDateTimeWidget():
    return DateTimeWidget(usel10n=False, bootstrap_version=3, options={'format': 'yyyy-mm-dd hh:ii', 'startView':4, 'language':'es'})

# Función que retorna el selector de hora
def MyTimeWidget():
    return TimeWidget(usel10n=False, bootstrap_version=3, options={'format': 'hh:ii', 'startView':1, 'language':'es'})   


