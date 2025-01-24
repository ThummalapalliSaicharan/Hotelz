from django.contrib import admin
from .models import Booking,Room,MyBookings,Contactus,Feedback,BankDetails,ReturnAmount

# Register your models here.
admin.site.register(Booking)
admin.site.register(Room)
admin.site.register(MyBookings)
admin.site.register(Contactus)
admin.site.register(Feedback)
admin.site.register(BankDetails)
admin.site.register(ReturnAmount)



