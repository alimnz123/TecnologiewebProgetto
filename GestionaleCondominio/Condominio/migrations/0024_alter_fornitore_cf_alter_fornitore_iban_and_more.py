# Generated by Django 5.1.1 on 2024-10-08 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Condominio', '0023_alter_verbale_lettera_accompagnatoria'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fornitore',
            name='cf',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='fornitore',
            name='iban',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='fornitore',
            name='indirizzo',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='fornitore',
            name='partita_iva',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='fornitore',
            name='ragione_sociale',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
