from cProfile import label
from tkinter import Widget
from turtle import width
from django import forms
from Equipos.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms.widgets import DateInput, TimeInput
from .models import Partidos



class EquiposFormulario(forms.Form):
    nombre = forms.CharField(max_length=30)
    abreviatura = forms.CharField(max_length=8)
    nombre_DT = forms.CharField(label='Nombre completo DT', max_length=20)
    cant_jugadores = forms.IntegerField(
        label='Cantidad de jugadores', max_value=35)
    escudo = forms.ImageField(required=False)
    torneo_equipo = forms.ModelChoiceField(Torneos.objects.all())


class JugadoresFormulario(forms.Form):
    nombre = forms.CharField(label='Nombre', max_length=30)
    apellido = forms.CharField(label='Apellido', max_length=30)
    dorsal = forms.IntegerField(label='Dorsal', max_value=99)
    equipo = forms.ModelChoiceField(
        label='Equipo', queryset=Equipos.objects.all())
    posicion = forms.ModelChoiceField(
        label='Posicion', queryset=PosicionesJugadores.objects.all())


class RegisterForm(UserCreationForm):

    first_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Nombre', 'class': 'form-control', }))

    last_name = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Apellido', 'class': 'form-control', }))

    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': 'Usuario', 'class': 'form-control', }))

    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-control', }))

    password1 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña', 'class': 'form-control', 'data-toggle': 'password', 'id': 'password', }))

    password2 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar contraseña', 'class': 'form-control', 'data-toggle': 'password', 'id': 'password', }))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'placeholder': '', 'class': 'form-control', }))

    password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput(attrs={'placeholder': '','class': 'form-control','data-toggle': 'password','id': 'password','name': 'password',}))

    remember_me = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ['username', 'password', 'remember_me']



class UserEditForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    username = forms.CharField(label='Nombre de Usuario')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'username']
        help_texts = {k:"" for k in fields}



class EditarResultadoForm(forms.Form):
    resultado = forms.CharField(max_length=10)


class PartidoForm(forms.ModelForm):
    fecha = forms.DateField(widget=DateInput(attrs={'type': 'date'}))
    hora = forms.TimeField(widget=TimeInput(attrs={'type': 'time'}))

    def __init__(self, *args, **kwargs):
        equipos = kwargs.pop('equipos', None)
        super(PartidoForm, self).__init__(*args, **kwargs)

        if equipos:
            self.fields['equipo_local'].queryset = equipos
            self.fields['equipo_visitante'].queryset = equipos

    class Meta:
        model = Partidos
        fields = ['fecha', 'hora', 'equipo_local', 'equipo_visitante', 'resultado']


class TablaPosicionesForm(forms.ModelForm):
    class Meta:
        model = TablaPosiciones
        fields = '__all__' 
