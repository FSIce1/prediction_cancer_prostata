# Generated by Django 4.0.4 on 2023-12-19 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analisis', '0003_analisisimagen_resultado_analisisimagen_tiempo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Logs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('funcion', models.CharField(default='', max_length=150)),
                ('resultado', models.CharField(default='', max_length=150)),
            ],
        ),
    ]
