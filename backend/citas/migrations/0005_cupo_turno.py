# Generated by Django 5.1.7 on 2025-03-12 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('citas', '0004_alter_personal_cargo'),
    ]

    operations = [
        migrations.AddField(
            model_name='cupo',
            name='turno',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
