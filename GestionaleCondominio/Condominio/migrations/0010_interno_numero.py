# Generated by Django 5.0.6 on 2024-08-26 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Condominio', '0009_interno_millesimi_edificio'),
    ]

    operations = [
        migrations.AddField(
            model_name='interno',
            name='numero',
            field=models.IntegerField(default=1, verbose_name='Numero'),
            preserve_default=False,
        ),
    ]
