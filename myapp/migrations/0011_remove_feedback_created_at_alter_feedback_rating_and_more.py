# Generated by Django 5.0.2 on 2024-10-26 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_feedback'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='feedback',
            name='rating',
            field=models.PositiveIntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')]),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='user_name',
            field=models.CharField(max_length=255),
        ),
    ]
