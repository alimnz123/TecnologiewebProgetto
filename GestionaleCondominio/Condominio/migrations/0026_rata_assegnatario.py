# Generated by Django 5.1.2 on 2024-10-20 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Condominio', '0025_rata'),
    ]

    operations = [
        migrations.AddField(
            model_name='rata',
            name='assegnatario',
            field=models.ManyToManyField(to='Condominio.interno'),
        ),
    ]
