# Generated by Django 5.0.6 on 2024-08-23 16:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Condominio', '0007_spesa'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(verbose_name='Hai un nuovo messaggio in bacheca')),
            ],
        ),
        migrations.AlterField(
            model_name='spesa',
            name='fornitore',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='Condominio.fornitore'),
        ),
        migrations.CreateModel(
            name='UserNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('is_seen', models.BooleanField()),
                ('notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Condominio.notification')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='notification',
            name='users',
            field=models.ManyToManyField(through='Condominio.UserNotification', to=settings.AUTH_USER_MODEL),
        ),
    ]