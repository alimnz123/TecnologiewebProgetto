# Generated by Django 5.1.1 on 2024-09-16 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Condominio', '0022_alter_documentipalazzo_file_documento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verbale',
            name='lettera_accompagnatoria',
            field=models.FileField(blank=True, default=None, upload_to='lettereAccompagnatorie', verbose_name='Lettera accompagnatoria'),
        ),
    ]