# Generated by Django 4.2.6 on 2023-10-26 01:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('abreviatura', models.CharField(max_length=8)),
                ('nombre_DT', models.CharField(max_length=20)),
                ('cant_jugadores', models.IntegerField()),
                ('escudo', models.ImageField(blank=True, null=True, upload_to='Equipos/escudos/')),
            ],
        ),
        migrations.CreateModel(
            name='PosicionesJugadores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('posicion', models.CharField(max_length=35)),
            ],
        ),
        migrations.CreateModel(
            name='Torneos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('cantidad_equipos', models.IntegerField()),
                ('cantidad_jugadores_por_lado', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Partidos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('equipo_local', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partidos_locales', to='Equipos.equipos')),
                ('equipo_visitante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='partidos_visitantes', to='Equipos.equipos')),
                ('torneo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Equipos.torneos')),
            ],
        ),
        migrations.CreateModel(
            name='Jugadores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('apellido', models.CharField(max_length=30)),
                ('dorsal', models.IntegerField()),
                ('equipo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Equipos.equipos')),
                ('posicion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Equipos.posicionesjugadores')),
            ],
        ),
        migrations.AddField(
            model_name='equipos',
            name='torneo_equipo',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Equipos.torneos'),
        ),
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='Avatar/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
