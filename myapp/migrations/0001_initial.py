# Generated by Django 5.0.2 on 2024-06-29 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('useremail', models.CharField(max_length=50)),
                ('phoneno', models.CharField(max_length=10)),
                ('numberofrooms', models.IntegerField(verbose_name=10)),
                ('location', models.CharField(choices=[('Delhi', 'Delhi'), ('Kolkata', 'Kolkata'), ('Mumbai', 'Mumbai'), ('Pune', 'Pune'), ('Lucknow', 'Lucknow'), ('Ahmedabad', 'Ahmedabad'), ('Hyderabad', 'Hyderabad'), ('Vijayawada', 'Vijayawada'), ('Chennai', 'Chennai'), ('Bangalore', 'Bangalore'), ('Amaravati', 'Amaravati'), ('Thiruvananthapuram', 'Thiruvananthapuram')], max_length=20)),
                ('roomtype', models.CharField(choices=[('Delux', 'Delux'), ('SuperDelux', 'SuperDelux'), ('Suite', 'Suite')], max_length=20)),
                ('fromdate', models.DateField()),
                ('todate', models.DateField()),
            ],
        ),
    ]
