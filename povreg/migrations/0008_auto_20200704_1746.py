# Generated by Django 2.1.1 on 2020-07-04 21:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('povreg', '0007_auto_20200628_1410'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='user',
            field=models.OneToOneField(help_text='This is the user account that corresponds to the driver', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='driver',
            name='verified',
            field=models.BooleanField(default=False, help_text='whether driver data is verified by admin'),
        ),
        migrations.AddField(
            model_name='officer',
            name='user',
            field=models.OneToOneField(help_text='this is the user account connected to this officer', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='officer',
            name='verified',
            field=models.BooleanField(default=False, help_text='whether driver data is verified by admin'),
        ),
        migrations.AlterField(
            model_name='car',
            name='status',
            field=models.TextField(choices=[('go', 'good'), ('st', 'stolen')], default='go', help_text="vehicle's current reported status"),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='status',
            field=models.TextField(choices=[('su', 'Suspended'), ('ac', 'Active'), ('ex', 'Expired')], default='ac', help_text="vehicle's current insurance status"),
        ),
    ]
