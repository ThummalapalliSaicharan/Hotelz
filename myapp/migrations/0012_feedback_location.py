# Generated by Django 5.0.2 on 2024-11-02 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0011_remove_feedback_created_at_alter_feedback_rating_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='location',
            field=models.CharField(choices=[('Delhi', 'Delhi'), ('Kolkata', 'Kolkata'), ('Mumbai', 'Mumbai'), ('Pune', 'Pune'), ('Lucknow', 'Lucknow'), ('Ahmedabad', 'Ahmedabad'), ('Hyderabad', 'Hyderabad'), ('Vijayawada', 'Vijayawada'), ('Chennai', 'Chennai'), ('Bangalore', 'Bangalore'), ('Amaravati', 'Amaravati'), ('Thiruvananthapuram', 'Thiruvananthapuram')], default=1, max_length=20),
            preserve_default=False,
        ),
    ]
