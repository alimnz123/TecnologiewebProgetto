# Generated by Django 5.0.6 on 2024-07-29 22:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Condominio', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Interno',
            fields=[
                ('numero', models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='Numero')),
                ('millesimi_generali', models.FloatField(verbose_name='Millesimi generali')),
                ('millesimi_scala', models.FloatField(verbose_name='Millesimi Scala')),
                ('in_affitto', models.BooleanField(verbose_name='In affitto')),
                ('mappali', models.CharField(max_length=100, verbose_name='Mappali')),
                ('condomino', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]