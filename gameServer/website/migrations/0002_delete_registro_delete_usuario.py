# Generated by Django 4.1.7 on 2023-03-31 16:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Registro',
        ),
        migrations.DeleteModel(
            name='Usuario',
        ),
    ]
