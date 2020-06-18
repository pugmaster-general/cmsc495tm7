# Generated by Django 2.1.1 on 2020-06-18 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('povreg', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='status',
            field=models.TextField(choices=[('st', 'stolen'), ('go', 'good')], default='go', help_text="vehicle's current reported status"),
        ),
        migrations.AlterField(
            model_name='insurance',
            name='status',
            field=models.TextField(choices=[('ac', 'Active'), ('su', 'Suspended'), ('ex', 'Expired')], default='ac', help_text="vehicle's current insurance status"),
        ),
    ]