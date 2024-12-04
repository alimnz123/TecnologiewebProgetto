# Generated by Django 5.1.3 on 2024-12-04 15:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Condominio', '0030_alter_lettera_convocazione_convocazione_documento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='documentipalazzo',
            name='data',
            field=models.DateField(primary_key=True, serialize=False, verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='lettera_convocazione',
            name='data',
            field=models.DateField(primary_key=True, serialize=False, verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='spesa',
            name='data',
            field=models.DateField(verbose_name='Data'),
        ),
    ]
