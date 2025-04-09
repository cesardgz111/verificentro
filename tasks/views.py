from django.shortcuts import render, redirect
from .models import Vehiculo, Cita

def verificacion(request):
    return render(request, "verificacion-vehicular.html")

def cancelar(request):
    return render(request, "cancelar-cita.html")

def holograma_exento(request):
    if request.method == 'POST':
        # Datos del vehículo
        placa = request.POST.get('placa', '').strip()
        serie = request.POST.get('serie', '').strip()
        marca = request.POST.get('marca', '').strip()
        submarca = request.POST.get('submarca', '').strip()
        modelo = request.POST.get('modelo', '').strip()
        nombre_solicitante = request.POST.get('nombre_solicitante', '').strip()
        correo = request.POST.get('correo', '').strip()

        # DEBUG: Imprimir los valores recibidos
        print(f"Placa: {placa}, Serie: {serie}, Marca: {marca}")

        if not placa:
            return render(request, 'verificacion-vehicular.html', {
                "error": "La placa es obligatoria."
            })

        # Buscar o crear vehículo
        vehiculo, created = Vehiculo.objects.get_or_create(
            placa=placa,
            defaults={
                "serie": serie,
                "marca": marca,
                "submarca": submarca,
                "modelo": modelo,
                "dueño": nombre_solicitante,
                "correo": correo,
            }
        )

        # Guardar en sesión y redirigir
        request.session['vehiculo_id'] = vehiculo.id
        return redirect('seleccion_cita')
    
    return render(request, 'holograma-exento.html')

def constancia_d(request):
    if request.method == 'POST':
        # Datos del vehículo
        placa = request.POST.get('placa', '').strip()
        serie = request.POST.get('serie', '').strip()
        marca = request.POST.get('marca', '').strip()
        submarca = request.POST.get('submarca', '').strip()
        modelo = request.POST.get('modelo', '').strip()
        nombre_solicitante = request.POST.get('nombre_solicitante', '').strip()
        correo = request.POST.get('correo', '').strip()

        # DEBUG: Imprimir los valores recibidos
        print(f"Placa: {placa}, Serie: {serie}, Marca: {marca}")

        if not placa:
            return render(request, 'verificacion-vehicular.html', {
                "error": "La placa es obligatoria."
            })

        # Buscar o crear vehículo
        vehiculo, created = Vehiculo.objects.get_or_create(
            placa=placa,
            defaults={
                "serie": serie,
                "marca": marca,
                "submarca": submarca,
                "modelo": modelo,
                "dueño": nombre_solicitante,
                "correo": correo,
            }
        )

        # Guardar en sesión y redirigir
        request.session['vehiculo_id'] = vehiculo.id
        return redirect('seleccion_cita')
    
    return render(request,"constancia-d.html")

def verificacion_extemporanea(request):
    if request.method == 'POST':
        # Datos del vehículo
        placa = request.POST.get('placa', '').strip()
        serie = request.POST.get('serie', '').strip()
        marca = request.POST.get('marca', '').strip()
        submarca = request.POST.get('submarca', '').strip()
        modelo = request.POST.get('modelo', '').strip()
        nombre_solicitante = request.POST.get('nombre_solicitante', '').strip()
        correo = request.POST.get('correo', '').strip()

        # DEBUG: Imprimir los valores recibidos
        print(f"Placa: {placa}, Serie: {serie}, Marca: {marca}")

        if not placa:
            return render(request, 'verificacion-vehicular.html', {
                "error": "La placa es obligatoria."
            })

        # Buscar o crear vehículo
        vehiculo, created = Vehiculo.objects.get_or_create(
            placa=placa,
            defaults={
                "serie": serie,
                "marca": marca,
                "submarca": submarca,
                "modelo": modelo,
                "dueño": nombre_solicitante,
                "correo": correo,
            }
        )

        # Guardar en sesión y redirigir
        request.session['vehiculo_id'] = vehiculo.id
        return redirect('seleccion_cita')
    
    return render(request,"verificacion-extemporanea.html")

def index(request):
    return render(request, 'principal.html')

def citas(request):
    if request.method == 'POST':
        # Captura de datos desde el formulario
        placa = request.POST.get('placa', '').strip()
        serie = request.POST.get('serie', '').strip()
        marca = request.POST.get('marca', '').strip()
        submarca = request.POST.get('submarca', '').strip()
        modelo = request.POST.get('modelo', '').strip()
        nombre_solicitante = request.POST.get('nombre_solicitante', '').strip()
        correo = request.POST.get('correo', '').strip()

        # Verificar si el vehículo existe en la base de datos
        try:
            vehiculo = Vehiculo.objects.get(
                placa=placa,
                serie=serie,
                marca=marca,
                submarca=submarca,
                modelo=modelo,
                dueño=nombre_solicitante,
                correo=correo
            )
        except Vehiculo.DoesNotExist:
            # Si no se encuentra, se muestra un error en la página de verificación vehicular
            return render(request, 'verificacion-vehicular.html', {
                "error": "Vehículo no encontrado. Verifica que los datos ingresados sean correctos."
            })

        # Si se encuentra el vehículo, se guarda su id en la sesión y se redirige a la pantalla de selección de cita
        request.session['vehiculo_id'] = vehiculo.id
        return redirect('seleccion_cita')

    return render(request, 'verificacion-vehicular.html')



def seleccion_cita(request):
    if request.method == 'POST':
        # Recuperar el ID del vehículo desde la sesión
        vehiculo_id = request.session.get('vehiculo_id')
        if not vehiculo_id:
            return redirect('verificacion')  # Si no hay vehículo, redirigir

        municipio = request.POST.get('municipio')
        verificentro = request.POST.get('verificentro')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')

        vehiculo = Vehiculo.objects.get(id=vehiculo_id)

        # Crear la cita con el vehículo relacionado
        Cita.objects.create(
            vehiculo=vehiculo,
            municipio=municipio,
            verificentro=verificentro,
            fecha=fecha,
            hora=hora
        )

        # Eliminar la sesión después de agendar la cita
        del request.session['vehiculo_id']

        return redirect('index')  # Redirigir a la página principal

    else:
        vehiculo_id = request.session.get('vehiculo_id')
        if vehiculo_id:
            vehiculo = Vehiculo.objects.get(id=vehiculo_id)
            return render(request, 'citas.html', {'datos_cita': vehiculo})
        else:
            return redirect('verificacion')  # Si no hay vehículo en sesión, redirigir