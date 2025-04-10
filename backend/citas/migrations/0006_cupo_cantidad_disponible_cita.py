# Generated by Django 5.1.7 on 2025-04-06 06:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0005_cupo_turno'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='cupo',
            name='cantidad_disponible',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Cita',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni_paciente', models.CharField(max_length=20)),
                ('fecha_registro', models.DateTimeField(auto_now_add=True)),
                ('ip_registro', models.GenericIPAddressField(blank=True, null=True)),
                ('cupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='citas.cupo')),
                ('usuario_registro', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='citas_registradas', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
