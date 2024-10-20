# Generated by Django 5.1.2 on 2024-10-20 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Condominio', '0024_alter_fornitore_cf_alter_fornitore_iban_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_scadenza', models.DateTimeField(verbose_name='Data')),
                ('descrizione', models.CharField(default=None, max_length=300)),
                ('importo', models.FloatField(default=None)),
                ('pagata', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'Rate',
            },
        ),
    ]