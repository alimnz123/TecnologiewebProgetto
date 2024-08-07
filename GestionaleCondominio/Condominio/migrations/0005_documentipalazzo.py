# Generated by Django 5.0.6 on 2024-08-07 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Condominio', '0004_lettera_convocazione_verbale'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentiPalazzo',
            fields=[
                ('data', models.DateTimeField(primary_key=True, serialize=False, verbose_name='Data')),
                ('descrizione', models.CharField(max_length=200)),
                ('file_documento', models.FileField(blank=True, default=None, upload_to='', verbose_name='Documento del Palazzo')),
            ],
            options={
                'verbose_name_plural': 'Documenti del Palazzo',
            },
        ),
    ]
