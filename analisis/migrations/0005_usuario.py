# Generated by Django 4.0.4 on 2024-01-14 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analisis', '0004_logs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(default='', max_length=150)),
                ('password', models.CharField(default='', max_length=150)),
            ],
        ),
    ]
