
from typing import List
from django.shortcuts import redirect, render,redirect, get_object_or_404
from Equipos.models import Equipos, Jugadores
from Equipos.forms import RegisterForm, LoginForm, UserEditForm

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib import messages
from django.contrib.auth.views import LoginView


from .forms import EditarResultadoForm, PartidoForm
from .models import Partidos, Torneos
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404

from .models import TablaPosiciones
from .forms import TablaPosicionesForm
from django.shortcuts import render
from .models import TablaPosiciones



def inicio(request):
    return render(request, "inicio.html")


def buscarJugador(request):
    if request.GET:
        nombre = request.GET['nombre']
        jugadores = Jugadores.objects.filter(nombre__icontains=nombre)
        return render(request, "jugadoresBuscar.html", {"jugadores": jugadores, "nombre": nombre})


def buscarEquipo(request):
    if request.GET:
        nombre = request.GET['nombre']
        equipos = Equipos.objects.filter(nombre__icontains=nombre)
        return render(request, "equiposBuscar.html", {"equipos": equipos, "nombre": nombre})


class EquiposList(ListView):

    model = Equipos
    template_name = "equipos.html"


class EquipoDetalle(DetailView):

    model = Equipos
    template_name = "equipo_detalle.html"


class EquipoCreacion(LoginRequiredMixin, CreateView):

    model = Equipos
    success_url = "/equipos/"
    fields = ['nombre', 'nombre_DT', 'abreviatura', 'cant_jugadores', 'escudo', 'torneo_equipo']
    template_name_suffix = '_nuevo'


class EquipoEditar(LoginRequiredMixin, UpdateView):

    model = Equipos
    success_url = "/equipos/"
    fields = ['nombre', 'nombre_DT', 'abreviatura', 'cant_jugadores', 'escudo', 'torneo_equipo']
    template_name_suffix = '_actualizar'


class EquipoEliminar(LoginRequiredMixin, DeleteView):

    model = Equipos
    success_url = "/equipos/"
    template_name_suffix = '_eliminar'


class JugadoresList(ListView):

    model = Jugadores
    template_name = "jugadores.html"


class JugadorCreacion(LoginRequiredMixin, CreateView):

    model = Jugadores
    success_url = "/jugadores/"
    fields = ['nombre', 'apellido', 'dorsal', 'equipo', 'posicion']
    template_name_suffix = '_nuevo'


class JugadorEditar(LoginRequiredMixin, UpdateView):

    model = Jugadores
    success_url = "/jugadores/"
    fields = ['nombre', 'apellido', 'dorsal', 'equipo', 'posicion']
    template_name_suffix = '_actualizar'


class JugadorEliminar(LoginRequiredMixin, DeleteView):

    model = Jugadores
    success_url = "/jugadores/"
    template_name_suffix = '_eliminar'


class JugadoresEquipo(ListView):

    model = Jugadores
    template_name = "equipo_detalle_jugadores.html"

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Usuario creado exitosamente: {username}')

            return redirect(to='/')

        return render(request, self.template_name, {'form': form})

class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)

            self.request.session.modified = True

        return super(CustomLoginView, self).form_valid(form)

def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            return redirect(to='/')

        return super(RegisterView, self).dispatch(request, *args, **kwargs)

def torneos(request):
    return render(request, "Torneos/torneos.html")

def torneonavideno(request):
    #filtrar solo los equipos que tengan torneo_equipo = futbol5
    equipos = Equipos.objects.filter(torneo_equipo=1)
    torneo = Torneos.objects.get(id=1)
    return render(request, "Torneos/torneonavideno.html", {"equipos": equipos, "torneo":torneo})

def torneoregular(request):
    equipos = Equipos.objects.filter(torneo_equipo=2)
    torneo = Torneos.objects.get(id=2)
    return render(request, "Torneos/torneoregular.html", {"equipos": equipos, "torneo":torneo})

def torneoregular2(request):
    equipos = Equipos.objects.filter(torneo_equipo=3)
    torneo = Torneos.objects.get(id=3)
    return render(request, "Torneos/torneoregular2.html", {"equipos": equipos, "torneo":torneo})

def construccion(request):
    return render(request, "construccion.html")

def about(request):
    return render(request, "about.html")

@login_required    
def editarPerfil(request):
    
    usuario = request.user

    if request.method == 'POST':
        miFormulario = UserEditForm(request.POST, instance=usuario)
        if miFormulario.is_valid():
            informacion = miFormulario.cleaned_data

            usuario.email = informacion['email']
            usuario.password1 = informacion['password1']
            usuario.username = informacion['username']
            usuario.save()

            return render(request, "inicio.html", {"usuario": usuario})
    else:
        miFormulario = UserEditForm({'email': usuario.email, 'first_name': usuario.first_name, 'last_name': usuario.last_name})
    return render(request, "editar_perfil.html", {"miFormulario": miFormulario, "usuario": usuario})


def crear_partido(request, torneo_id):
    torneo = Torneos.objects.get(id=torneo_id)
    if request.method == 'POST':
        form = PartidoForm(request.POST)
        if form.is_valid():
            partido = form.save(commit=False)
            partido.torneo = torneo
            partido.save()
            return redirect('tabla_partidos', torneo_id=torneo_id)
    else:
        form = PartidoForm()
    
    return render(request, 'crear_partido.html', {'form': form, 'torneo':torneo})
                                                  

def tabla_partidos(request, torneo_id):
    torneo = Torneos.objects.get(id=torneo_id)
    partidos = Partidos.objects.filter(torneo=torneo)
    paginator = Paginator(partidos, 10)
    page = request.GET.get('page')
    partidos = paginator.get_page(page)

    return render(request, 'tabla_partidos.html', {'torneo': torneo, 'partidos': partidos})






def editar_partido(request, torneo_id, partido_id):
    torneo = get_object_or_404(Torneos, id=torneo_id)
    partido = get_object_or_404(Partidos, id=partido_id)

    if request.method == 'POST':
        form = PartidoForm(request.POST, instance=partido)
        if form.is_valid():
            form.save()
            return redirect('tabla_partidos', torneo_id=torneo_id)
    else:
        # Formatea la fecha en el formato "yyyy-MM-dd"
        formatted_fecha = partido.fecha.strftime('%Y-%m-%d')
        partido.fecha = formatted_fecha
        form = PartidoForm(instance=partido, equipos=Equipos.objects.filter(torneo_equipo=torneo))

    return render(request, 'editar_partido.html', {'form': form, 'partido': partido})


def crear_partido(request, torneo_id):
    torneo = Torneos.objects.get(id=torneo_id)
    equipos = Equipos.objects.filter(torneo_equipo=torneo)  # Obtiene los equipos asociados al torneo
    if request.method == 'POST':
        form = PartidoForm(request.POST, equipos=equipos)  # Pasa los equipos al formulario
        if form.is_valid():
            partido = form.save(commit=False)
            partido.torneo_id = torneo_id
            partido.save()
            return redirect('tabla_partidos', torneo_id=torneo_id)
    else:
        form = PartidoForm(equipos=equipos)  # Pasa los equipos al formulario

    return render(request, 'crear_partido.html', {'form': form, 'torneo_id': torneo_id})



def eliminar_partido(request, torneo_id, partido_id):
    torneo = get_object_or_404(Torneos, id=torneo_id)
    partido = get_object_or_404(Partidos, id=partido_id)

    if request.method == 'POST':
        # Realizar la eliminación del partido
        partido.delete()
        return redirect('tabla_partidos', torneo_id=torneo_id)

    return redirect('tabla_partidos', torneo_id=torneo_id)

def crear_tabla_posiciones(request, torneo_id):
    if request.method == 'POST':
        form = TablaPosicionesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ver_tabla_posiciones', torneo_id=torneo_id)
    else:
        form = TablaPosicionesForm()
    
    context = {
        'form': form,
        'torneo_id': torneo_id,
    }

    return render(request, 'crear_tabla_posiciones.html', context)

def editar_tabla_posiciones(request, torneo_id, posicion_id):
    posicion = get_object_or_404(TablaPosiciones, id=posicion_id)
    if request.method == 'POST':
        form = TablaPosicionesForm(request.POST, instance=posicion)
        if form.is_valid():
            form.save()
            return redirect('ver_tabla_posiciones', torneo_id=torneo_id)
    else:
        form = TablaPosicionesForm(instance=posicion)
    
    context = {
        'form': form,
        'torneo_id': torneo_id,
        'posicion_id': posicion_id,
    }

    return render(request, 'editar_tabla_posiciones.html', context)

def eliminar_tabla_posiciones(request, torneo_id, posicion_id):
    posicion = get_object_or_404(TablaPosiciones, id=posicion_id)
    if request.method == 'POST':
        posicion.delete()
        return redirect('ver_tabla_posiciones', torneo_id=torneo_id)
    
    context = {
        'posicion': posicion,
        'torneo_id': torneo_id,
    }

    return render(request, 'eliminar_tabla_posiciones.html', context)



def tabla_posiciones(request, torneo_id):
    # Obtener todos los registros de la tabla de posiciones para el torneo especificado
    posiciones = TablaPosiciones.objects.filter(torneo_id=torneo_id)

    # Puedes realizar otras operaciones aquí, como ordenar los equipos por puntos, partidos jugados, etc.

    return render(request, 'tabla_posiciones.html', {'posiciones': posiciones, 'torneo_id': torneo_id})


def tabla_posicionesregulares(request):
    # Lógica para mostrar la tabla de posiciones para torneos regulares
    # Asegúrate de que esta vista tenga una lógica adecuada

    return render(request, 'tabla_posiciones.html')