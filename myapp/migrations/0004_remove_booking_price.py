# Generated by Django 5.0.2 on 2024-06-29 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_booking_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='price',
        ),
    ]
