# Generated by Django 5.0.6 on 2024-08-05 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Condominio', '0003_rename_numero_interno_numero_interno_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lettera_Convocazione',
            fields=[
                ('data', models.DateTimeField(primary_key=True, serialize=False, verbose_name='Data')),
                ('descrizione', models.CharField(max_length=200)),
                ('convocazione_documento', models.FileField(blank=True, default=None, upload_to='', verbose_name='Lettera di convocazione')),
            ],
            options={
                'verbose_name_plural': 'Lettere di convocazione',
            },
        ),
        migrations.CreateModel(
            name='Verbale',
            fields=[
                ('data', models.DateTimeField(primary_key=True, serialize=False, verbose_name='Data')),
                ('descrizione', models.CharField(max_length=200)),
                ('documento', models.FileField(blank=True, default=None, upload_to='', verbose_name='Documento')),
                ('lettera_accompagnatoria', models.FileField(blank=True, default=None, upload_to='', verbose_name='Lettera accompagnatoria')),
            ],
            options={
                'verbose_name_plural': 'Verbali',
                'ordering': ['data'],
            },
        ),
    ]
