# Generated by Django 5.1.2 on 2024-10-20 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Condominio', '0026_rata_assegnatario'),
    ]

    operations = [
        migrations.AddField(
            model_name='rata',
            name='file_pagamento',
            field=models.FileField(blank=True, default=None, upload_to='pagamenti/', verbose_name='File del pagamento'),
        ),
    ]
