# Generated by Django 5.1.7 on 2025-04-06 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0006_cupo_cantidad_disponible_cita'),
    ]

    operations = [
        migrations.AddField(
            model_name='cita',
            name='numero_solicitud',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
