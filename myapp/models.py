from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


# Create your models here.

LOCATION_CHOICES = (
    ("Delhi", "Delhi"),
    ("Kolkata", "Kolkata"),
    ("Mumbai", "Mumbai"),
    ("Pune", "Pune"),
    ("Lucknow", "Lucknow"),
    ("Ahmedabad", "Ahmedabad"),
    ("Hyderabad", "Hyderabad"),
    ("Vijayawada", "Vijayawada"),
    ("Chennai", "Chennai"),
    ("Bangalore", "Bangalore"),
    ("Amaravati", "Amaravati"),
    ("Thiruvananthapuram", "Thiruvananthapuram"),
)

ROOM_TYPE = (
    ("Delux", "Delux"),
    ("SuperDelux", "SuperDelux"),
    ("Suite", "Suite"),
)



class Room(models.Model):
    location = models.CharField(max_length=20, choices=LOCATION_CHOICES)
    roomtype = models.CharField(max_length=20, choices=ROOM_TYPE)
    total_rooms = models.IntegerField()
    available_rooms = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.location} - {self.roomtype}"

    def decrease_availability(self, num_rooms):
        if self.available_rooms >= num_rooms:
            self.available_rooms -= num_rooms
            self.save()
            return True
        return False

    def increase_availability(self, num_rooms):
        if self.available_rooms + num_rooms <= self.total_rooms:
            self.available_rooms += num_rooms
            self.save()
            return True
        return False

class Booking(models.Model):
    username = models.CharField(max_length=50)
    useremail = models.CharField(max_length=50)
    phoneno = models.CharField(max_length=10)
    numberofrooms = models.IntegerField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    fromdate = models.DateField()
    todate = models.DateField()
    payment = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.username} - {self.room.location} - {self.room.roomtype}"

    def save(self, *args, **kwargs):
        if not self.pk:  # Check if it's a new booking
            if self.room.decrease_availability(self.numberofrooms):
                super().save(*args, **kwargs)
            else:
                raise ValueError("Not enough available rooms")
        else:
            super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.room.increase_availability(self.numberofrooms)
        super().delete(*args, **kwargs)

class MyBookings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_id = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    fromdate = models.DateField()
    todate = models.DateField()
    payment_status = models.BooleanField(default=False)
    booked_on = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Active")

    def __str__(self):
        return f"Booking {self.booking_id} by {self.user.username} -  {self.status}"

class Contactus(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    subject = models.CharField(max_length=300)
    message = models.CharField(max_length=500)

    def __str__(self):
        return f" {self.email}"


from django.db import models

class Feedback(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]

    user_name = models.CharField(max_length=255)
    location = models.CharField(max_length=20)
    comments = models.TextField()  # Store feedback comments
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)  # Rating choices

    def __str__(self):
        return f'{self.user_name} - {self.location} - {self.rating} Stars'




class BankDetails(models.Model):
    user = models.CharField(max_length=50)
    account_holder_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    ifsc_code = models.CharField(max_length=11)

    # Contact details
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    is_submitted = models.BooleanField(default=False)


    def __str__(self):
        return f"Bank details of - {self.user}"

from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator

from decimal import Decimal


class ReturnAmount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking = models.OneToOneField('MyBookings', on_delete=models.CASCADE, related_name="return_amount")

    # Bank details fields
    account_holder_name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20, validators=[MinLengthValidator(10)])
    ifsc_code = models.CharField(max_length=11)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)

    refund_amount = models.DecimalField(max_digits=10,decimal_places=2)
    return_status = models.BooleanField(default=False)  # Added field for return status


    def __str__(self):
        return f"Return Amount {self.refund_amount} - for - {self.user.username} - Booking ID {self.booking.booking_id}"
