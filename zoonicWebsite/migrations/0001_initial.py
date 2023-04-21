# Generated by Django 4.1.7 on 2023-04-21 00:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recovers',
            fields=[
                ('username', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True, verbose_name='username')),
                ('token', models.CharField(max_length=36, unique=True, verbose_name='token')),
                ('time_created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='time created')),
            ],
        ),
    ]