# Generated by Django 5.0.2 on 2024-08-18 06:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_mybookings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mybookings',
            name='booking_id',
            field=models.CharField(max_length=50),
        ),
    ]
