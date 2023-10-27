from django.urls import path, include
from Equipos import views
from .views import RegisterView, CustomLoginView
from .forms import LoginForm
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name="Inicio"),
    path('jugadores/buscarJugador/', views.buscarJugador, name="buscarJugador"),

    path('equipos/', views.EquiposList.as_view(), name='Equipos'),
    path('equipos/buscarEquipo/', views.buscarEquipo, name="buscarEquipo"),
    path('equipos/<int:pk>/', views.EquipoDetalle.as_view(), name='DetalleEquipo'),
    path('equiposEditar/<int:pk>/', views.EquipoEditar.as_view(), name='EditarEquipo'),
    path('equiposBorrar/<int:pk>/', views.EquipoEliminar.as_view(), name='EliminarEquipo'),
    path('equiposNuevo/', views.EquipoCreacion.as_view(), name='NuevoEquipo'),

    path('jugadores/', views.JugadoresList.as_view(), name='Jugadores'),
    path('jugadoresNuevo/', views.JugadorCreacion.as_view(), name='NuevoJugador'),
    path('jugadoresEditar/<int:pk>/', views.JugadorEditar.as_view(), name='EditarJugador'),
    path('jugadoresBorrar/<int:pk>/', views.JugadorEliminar.as_view(), name='EliminarJugador'),

    path('torneos/', views.torneos, name="Torneos"),
    path('torneos/torneonavideno', views.torneonavideno, name="Torneonavideno"),
    path('torneos/torneoregular', views.torneoregular, name="Torneoregular"),
    path('torneos/torneoregular2', views.torneoregular2, name="Torneoregular2"),

    path("__reload__/", include("django_browser_reload.urls")),

    path('registro/', RegisterView.as_view(), name="Registro"),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='login.html', authentication_form=LoginForm), name="Login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name="Logout"),
    path('editarPerfil', views.editarPerfil, name="EditarPerfil"),

    path('oauth/', include('social_django.urls', namespace='social')),

    path('construccion/', views.construccion, name="Construccion"),
    path('about/', views.about, name="About"),

    path('crear_partido/<int:torneo_id>/', views.crear_partido, name='crear_partido'),
    path('tabla_partidos/<int:torneo_id>/', views.tabla_partidos, name='tabla_partidos'),
    path('editar_partido/<int:torneo_id>/<int:partido_id>//', views.editar_partido, name='editar_partido'),
    path('tabla_partidos/<int:torneo_id>/eliminar/<int:partido_id>/', views.eliminar_partido, name='eliminar_partido'),

    path('tabla_posiciones/', views.tabla_posicionesregulares, name='tabla_posiciones'),
    #path('tabla_posiciones/<int:torneo_id>/', views.tabla_posiciones, name='tabla_posiciones'),

    path('crear_tabla_posiciones/<int:torneo_id>/', views.crear_tabla_posiciones, name='crear_tabla_posiciones'),
    
    path('tabla_posiciones/', views.tabla_posicionesregulares, name='tabla_posiciones'),

    path('tabla_posiciones/<int:torneo_id>/', views.tabla_posiciones, name='tabla_posiciones'),

]
