# Generated by Django 4.0.4 on 2023-12-05 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analisis', '0002_paciente'),
    ]

    operations = [
        migrations.AddField(
            model_name='analisisimagen',
            name='resultado',
            field=models.CharField(default='', max_length=150, null=True),
        ),
        migrations.AddField(
            model_name='analisisimagen',
            name='tiempo',
            field=models.CharField(default='', max_length=150, null=True),
        ),
    ]
