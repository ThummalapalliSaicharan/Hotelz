# Generated by Django 5.0.2 on 2024-11-02 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_feedback_location'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='location',
            field=models.CharField(max_length=20),
        ),
    ]
