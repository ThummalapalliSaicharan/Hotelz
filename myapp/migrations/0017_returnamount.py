# Generated by Django 5.0.2 on 2024-11-02 13:03

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_bankdetails'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReturnAmount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_holder_name', models.CharField(max_length=100)),
                ('bank_name', models.CharField(max_length=100)),
                ('account_number', models.CharField(max_length=20, validators=[django.core.validators.MinLengthValidator(10)])),
                ('ifsc_code', models.CharField(max_length=11)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('refund_amount', models.DecimalField(decimal_places=2, editable=False, max_digits=10)),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='return_amount', to='myapp.mybookings')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
