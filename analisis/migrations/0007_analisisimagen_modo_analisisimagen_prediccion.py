# Generated by Django 4.0.4 on 2024-01-26 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analisis', '0006_rename_usuario_usuariologueo'),
    ]

    operations = [
        migrations.AddField(
            model_name='analisisimagen',
            name='modo',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='analisisimagen',
            name='prediccion',
            field=models.CharField(default='', max_length=150),
        ),
    ]
