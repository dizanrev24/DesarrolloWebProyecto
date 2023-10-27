
from email.mime import image
from django.db import models
from django.db.models import CharField, ImageField, IntegerField, ForeignKey, DateTimeField, TimeField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class Torneos(models.Model):
    nombre = CharField(max_length=30)
    cantidad_equipos = IntegerField()
    cantidad_jugadores_por_lado = IntegerField()

    def __str__(self):
        return f"{self.nombre}"
class Equipos(models.Model):
    nombre = CharField(max_length=30)
    abreviatura = CharField(max_length=8)
    nombre_DT = CharField(max_length=20)
    cant_jugadores = IntegerField()
    escudo = ImageField(upload_to='Equipos/escudos/', blank=True, null=True)
    torneo_equipo = ForeignKey(Torneos, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} / DT: {self.nombre_DT}"

class Partidos(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    equipo_local = models.ForeignKey(Equipos, on_delete=models.CASCADE, related_name='partidos_locales')
    equipo_visitante = models.ForeignKey(Equipos, on_delete=models.CASCADE, related_name='partidos_visitantes')
    torneo = models.ForeignKey(Torneos, on_delete=models.CASCADE)
    resultado = models.CharField(max_length=10, blank=True, null=True)
    pendiente = models.BooleanField(default=True)

    def _str_(self):
        return f"{self.equipo_local.nombre} vs {self.equipo_visitante.nombre} - {self.fecha} {self.hora}"


class PosicionesJugadores(models.Model):
    posicion = CharField(max_length=35)

    def __str__(self):
        return f"{self.posicion}"

class Jugadores(models.Model):
    nombre = CharField(max_length=30)
    apellido = CharField(max_length=30)
    dorsal = IntegerField()
    equipo = models.ForeignKey(Equipos, on_delete=models.CASCADE)
    posicion = models.ForeignKey(PosicionesJugadores, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido} / Dorsal: {self.dorsal} / {self.equipo.nombre} / {self.posicion}"


class Avatar(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = ImageField(upload_to='Avatar/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}"


class TablaPosiciones(models.Model):
    torneo = models.ForeignKey(Torneos, on_delete=models.CASCADE)  # Relación con el torneo
    equipo = models.ForeignKey(Equipos, on_delete=models.CASCADE)  # Relación con el equipo
    puntos = models.IntegerField()  # Puntos del equipo en el torneo
    partidos_jugados = models.IntegerField()  # Cantidad de partidos jugados por el equipo
    partidos_ganados = models.IntegerField()  # Cantidad de partidos ganados por el equipo
    partidos_empatados = models.IntegerField()  # Cantidad de partidos empatados por el equipo
    partidos_perdidos = models.IntegerField()  # Cantidad de partidos perdidos por el equipo
    goles_a_favor = models.IntegerField()  # Cantidad de goles a favor del equipo
    goles_en_contra = models.IntegerField()  # Cantidad de goles en contra del equipo

    def __str__(self):
        return f"{self.equipo.nombre} - {self.torneo.nombre}"

