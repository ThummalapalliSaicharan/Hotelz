from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.utils.encoding import force_str
from .utils import TokenGenerator, generate_token
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.generic import View
from django.core.mail import send_mail
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Booking, Room ,MyBookings,Contactus
import razorpay
import pkg_resources
from django.db.models import Avg
# Create your views here.

def index(request):
    return render(request,"index.html")

def loginpage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        validate_user = authenticate(username=username, password=password)
        if validate_user is not None:
            login(request, validate_user)
            return redirect('home')
        else:
            messages.error(request, "invalid credentials")
            return redirect('loginpage')
    return render(request,"login.html")

def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        cpassword = request.POST.get("cpassword")
        special_characters = {'[', ']', '{', '}', '(', ')', '/', '?', '.', ',', ';', ':', '|', '*', '~', '`',
                              '!', '^', '-', '_', '+', '<', '>', '@', '#', '$', '%', '&'}

        # Password constraints validation
        if len(password) < 8:
            messages.warning(request, "Password should be at least 8 characters")
            return redirect('register')
        if not any(char in special_characters for char in password):
            messages.warning(request, "Password should contain at least one special character.")
            return redirect('register')
        elif password != cpassword:
            messages.warning(request, "Passwords do not match.")
            return redirect('register')

        try:
            if User.objects.get(username=username):
                messages.warning(request, "UserName already taken")
                return redirect("register")
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(email=email):
                messages.warning(request, "Email already exists")
                return redirect("register")
        except User.DoesNotExist:
            pass

        user = User.objects.create_user(username, email, password)
        user.is_active = False
        user.save()

        email_subject = "Activate Your Account"
        message = render_to_string("activate.html", {
            "user": user,
            "domain": "127.0.0.1:8000",
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": generate_token.make_token(user)
        })

        email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
        email_message.send()

        messages.warning(request, "A confirmation email has been sent to your email.")
        return redirect('loginpage')

    return render(request,"register.html")

def about(request):
    return render(request,"about.html")


def service(request):
    return render(request,"service.html")

def rooms(request):
    return render(request,"rooms.html")

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        contact = Contactus(name=name, email=email, subject=subject, message=message)
        contact.save()
    return render(request,"contact.html")

@login_required()
def home(request):
    return render(request,"home.html")

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("loginpage")

        return render(request, "activatefail.html.html")

@login_required()
def delhi(request):
    delhi_rooms = Room.objects.filter(location="Delhi")

    # Calculate the total number of available rooms in Delhi
    total_available_rooms = sum(room.available_rooms for room in delhi_rooms)

    # Filter out the room types and any other information you want to display
    room_types = delhi_rooms.values('roomtype', 'available_rooms')  # Get the room types with their available rooms

    average_rating = Feedback.objects.filter(location="Delhi").aggregate(Avg('rating'))['rating__avg'] or 0
    average_rating = round(average_rating, 1)


    context = {
        'total_available_rooms': total_available_rooms,
        'room_types': room_types,  # Send room types data for dynamic display
        'average_rating': average_rating,
    }
    return render(request,"delhi.html",context)

@login_required()
def vijayawada(request):
    vij_rooms = Room.objects.filter(location="Vijayawada")

    # Calculate the total number of available rooms in Delhi
    total_available_rooms = sum(room.available_rooms for room in vij_rooms)

    # Filter out the room types and any other information you want to display
    room_types = vij_rooms.values('roomtype', 'available_rooms')  # Get the room types with their available rooms
    average_rating = Feedback.objects.filter(location="Vijayawada").aggregate(Avg('rating'))['rating__avg'] or 0
    average_rating = round(average_rating, 1)

    context = {
        'total_available_rooms': total_available_rooms,
        'room_types': room_types,  # Send room types data for dynamic display
        'average_rating': average_rating,
    }
    return render(request,"vijayawada.html",context)

@login_required()
def kolkata(request):
    kol_rooms = Room.objects.filter(location="Kolkata")

    # Calculate the total number of available rooms in Delhi
    total_available_rooms = sum(room.available_rooms for room in kol_rooms)

    # Filter out the room types and any other information you want to display
    room_types = kol_rooms.values('roomtype', 'available_rooms')  # Get the room types with their available rooms
    average_rating = Feedback.objects.filter(location="Kolkata").aggregate(Avg('rating'))['rating__avg'] or 0
    average_rating = round(average_rating, 1)

    context = {
        'total_available_rooms': total_available_rooms,
        'room_types': room_types,  # Send room types data for dynamic display
        'average_rating': average_rating,
    }
    return render(request,"kolkata.html",context)

@login_required()
def payment(request):
    return render(request,"payment.html")

@login_required()
def hyderabad(request):
    hyd_rooms = Room.objects.filter(location="Hyderabad")

    # Calculate the total number of available rooms in Delhi
    total_available_rooms = sum(room.available_rooms for room in hyd_rooms)

    # Filter out the room types and any other information you want to display
    room_types = hyd_rooms.values('roomtype', 'available_rooms')  # Get the room types with their available rooms
    average_rating = Feedback.objects.filter(location="Hyderabad").aggregate(Avg('rating'))['rating__avg'] or 0
    average_rating = round(average_rating, 1)

    context = {
        'total_available_rooms': total_available_rooms,
        'room_types': room_types,  # Send room types data for dynamic display
        'average_rating': average_rating,
    }
    return render(request,"hyderabad.html",context)

@login_required()
def chennai(request):
    che_rooms = Room.objects.filter(location="Chennai")

    # Calculate the total number of available rooms in Delhi
    total_available_rooms = sum(room.available_rooms for room in che_rooms)

    # Filter out the room types and any other information you want to display
    room_types = che_rooms.values('roomtype', 'available_rooms')  # Get the room types with their available rooms
    average_rating = Feedback.objects.filter(location="Chennai").aggregate(Avg('rating'))['rating__avg'] or 0
    average_rating = round(average_rating, 1)

    context = {
        'total_available_rooms': total_available_rooms,
        'room_types': room_types,  # Send room types data for dynamic display
        'average_rating': average_rating,
    }
    return render(request,"chennai.html",context)

@login_required()
def pune(request):
    _rooms = Room.objects.filter(location="Pune")

    # Calculate the total number of available rooms in Delhi
    total_available_rooms = sum(room.available_rooms for room in _rooms)

    # Filter out the room types and any other information you want to display
    room_types = _rooms.values('roomtype', 'available_rooms')  # Get the room types with their available rooms
    average_rating = Feedback.objects.filter(location="Pune").aggregate(Avg('rating'))['rating__avg'] or 0
    average_rating = round(average_rating, 1)

    context = {
        'total_available_rooms': total_available_rooms,
        'room_types': room_types,  # Send room types data for dynamic display
        'average_rating': average_rating,
    }
    return render(request,"pune.html",context)

@login_required()
def lucknow(request):
    _rooms = Room.objects.filter(location="Lucknow")

    # Calculate the total number of available rooms in Delhi
    total_available_rooms = sum(room.available_rooms for room in _rooms)

    # Filter out the room types and any other information you want to display
    room_types = _rooms.values('roomtype', 'available_rooms')  # Get the room types with their available rooms
    average_rating = Feedback.objects.filter(location="Lucknow").aggregate(Avg('rating'))['rating__avg'] or 0
    average_rating = round(average_rating, 1)

    context = {
        'total_available_rooms': total_available_rooms,
        'room_types': room_types,  # Send room types data for dynamic display
        'average_rating': average_rating,
    }
    return render(request,"lucknow.html",context)

@login_required()
def ahmedabad(request):
    _rooms = Room.objects.filter(location="Ahmedabad")

    # Calculate the total number of available rooms in Delhi
    total_available_rooms = sum(room.available_rooms for room in _rooms)

    # Filter out the room types and any other information you want to display
    room_types = _rooms.values('roomtype', 'available_rooms')  # Get the room types with their available rooms
    average_rating = Feedback.objects.filter(location="Ahmedabad").aggregate(Avg('rating'))['rating__avg'] or 0
    average_rating = round(average_rating, 1)

    context = {
        'total_available_rooms': total_available_rooms,
        'room_types': room_types,  # Send room types data for dynamic display
        'average_rating': average_rating,
    }
    return render(request,"ahmedabad.html",context)

@login_required()
def thiruvananthapuram(request):
    _rooms = Room.objects.filter(location="Thiruvananthapuram")

    # Calculate the total number of available rooms in Delhi
    total_available_rooms = sum(room.available_rooms for room in _rooms)

    # Filter out the room types and any other information you want to display
    room_types = _rooms.values('roomtype', 'available_rooms')  # Get the room types with their available rooms
    average_rating = Feedback.objects.filter(location="Thiruvananthapuram").aggregate(Avg('rating'))['rating__avg'] or 0
    average_rating = round(average_rating, 1)

    context = {
        'total_available_rooms': total_available_rooms,
        'room_types': room_types,  # Send room types data for dynamic display
        'average_rating': average_rating,
    }
    return render(request,"thiruvananthapuram.html",context)

@login_required()
def amaravati(request):
    _rooms = Room.objects.filter(location="Amaravati")

    # Calculate the total number of available rooms in Delhi
    total_available_rooms = sum(room.available_rooms for room in _rooms)

    # Filter out the room types and any other information you want to display
    room_types = _rooms.values('roomtype', 'available_rooms')  # Get the room types with their available rooms
    average_rating = Feedback.objects.filter(location="Amaravati").aggregate(Avg('rating'))['rating__avg'] or 0
    average_rating = round(average_rating, 1)

    context = {
        'total_available_rooms': total_available_rooms,
        'room_types': room_types,  # Send room types data for dynamic display
        'average_rating': average_rating,
    }
    return render(request,"amaravati.html",context)
@login_required()
def bangalore(request):
    _rooms = Room.objects.filter(location="Bangalore")

    # Calculate the total number of available rooms in Delhi
    total_available_rooms = sum(room.available_rooms for room in _rooms)

    # Filter out the room types and any other information you want to display
    room_types = _rooms.values('roomtype', 'available_rooms')  # Get the room types with their available rooms
    average_rating = Feedback.objects.filter(location="Bangalore").aggregate(Avg('rating'))['rating__avg'] or 0
    average_rating = round(average_rating, 1)

    context = {
        'total_available_rooms': total_available_rooms,
        'room_types': room_types,  # Send room types data for dynamic display
        'average_rating': average_rating,
    }
    return render(request,"bangalore.html",context)

@login_required()
def mumbai(request):
    _rooms = Room.objects.filter(location="Mumbai")

    # Calculate the total number of available rooms in Delhi
    total_available_rooms = sum(room.available_rooms for room in _rooms)

    # Filter out the room types and any other information you want to display
    room_types = _rooms.values('roomtype', 'available_rooms')  # Get the room types with their available rooms
    average_rating = Feedback.objects.filter(location="Mumbai").aggregate(Avg('rating'))['rating__avg'] or 0
    average_rating = round(average_rating, 1)

    context = {
        'total_available_rooms': total_available_rooms,
        'room_types': room_types,  # Send room types data for dynamic display
        'average_rating': average_rating,
    }
    return render(request,"mumbai.html",context)
@login_required()
def hotelzreception(request):
    return render(request,"hotelzreception.html")



def paymentsuccesspage(request):
    # Retrieve the booking_id from the session
    booking_id = request.session.get('booking_id')

    if not booking_id:
        return render(request, "error.html", {"message": "Booking ID not found in session."})

    try:
        booking = Booking.objects.get(id=booking_id)

        # Set payment status to True
        booking.payment = True
        booking.save()

        # Continue with storing booking details and sending email
        my_booking, created = MyBookings.objects.get_or_create(
            user=request.user,
            booking_id=booking_id,
            defaults={
                'amount': booking.amount,
                'room': booking.room,
                'fromdate': booking.fromdate,
                'todate': booking.todate,
                'payment_status': True
            }
        )

        if not created:
            my_booking.payment_status = True
            my_booking.save()

        pdf_buffer = generate_ticket_pdf(my_booking)

        email_subject = "Successfully Booked - Your Booking Details"
        email_body = f"Dear {request.user.username},\n\nYour booking has been successfully completed. Please find your booking details attached.\n\nThank you for choosing our service!\n\nBest Regards,\nHotelZ Team"
        email = EmailMessage(
            email_subject,
            email_body,
            settings.EMAIL_HOST_USER,
            [request.user.email]
        )
        email.attach(f"Booking_{booking_id}.pdf", pdf_buffer.getvalue(), "application/pdf")
        email.send()

    except Booking.DoesNotExist:
        return render(request, "error.html", {"message": "Booking matching query does not exist."})

    return render(request, "paymentsuccesspage.html", {
        'booking_id': booking.id,
        'amount': booking.amount
    })





import logging

@login_required()

def roombooking(request):
    if request.method == "POST":
        username = request.user.username
        useremail = request.user.email
        phoneno = request.POST.get('phoneno')
        numberofrooms = int(request.POST.get('numberofrooms'))
        room_id = request.POST.get('room_id')
        fromdate = datetime.strptime(request.POST.get('fromdate'), '%Y-%m-%d')
        todate = datetime.strptime(request.POST.get('todate'), '%Y-%m-%d')

        room = Room.objects.get(id=room_id)
        amount = room.price * numberofrooms

        # Calculate duration between fromdate and todate
        duration = (todate - fromdate).days + 1  # Adding 1 to include both start and end dates

        logging.debug(f"Initial available rooms: {room.available_rooms}")
        logging.debug(f"Number of rooms requested: {numberofrooms}")

        # Booking entry
        booking = Booking(
            username=username,
            useremail=useremail,
            phoneno=phoneno,
            numberofrooms=numberofrooms,
            room=room,
            amount=amount * duration,  # Multiply amount by duration
            fromdate=fromdate,
            todate=todate
        )

        # Decrease available rooms
        if numberofrooms <= room.available_rooms:  # Additional check
            room.available_rooms -= numberofrooms
        else:
            # Handle cases where requested rooms exceed available rooms
            logging.error("Requested more rooms than available!")
            return HttpResponse("Not enough rooms available!", status=400)

        logging.debug(f"Available rooms after booking: {room.available_rooms}")

        room.save()
        booking.save()
        request.session['booking_id'] = booking.id  # Store booking ID in session

        # Redirect to payment_form with booking details
        return payment_call(request, booking.id, booking.amount)

    # Handle GET request
    rooms = Room.objects.all()
    rooms_data = list(rooms.values('id', 'location', 'roomtype', 'price', 'available_rooms'))

    return render(request, "roombooking.html", {'rooms': rooms, 'rooms_data': rooms_data})


def payment_call(request, booking_id, amount):
    return render(request, 'payment.html', {'booking_id': booking_id, 'amount': amount})
@login_required()
def roominformation(request):
    return  render(request,"roominformation.html")
@login_required()
def logoutpage(request):
    logout(request)
    return redirect('loginpage')



from django.shortcuts import render, get_object_or_404




from .models import MyBookings


from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.utils import ImageReader
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import io

def download_ticket(request, booking_id):
    # Retrieve the booking
    booking = get_object_or_404(MyBookings, id=booking_id, user=request.user)

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Add the "BOOKED" image to the PDF
    img_path = "static/assets2/img/BOOKED-removebg-preview.png"  # Update the path to your image
    booked_img = Image(img_path, 2.5 * inch, 2.5 * inch)
    booked_img.hAlign = 'RIGHT'
    elements.append(booked_img)

    # Add a spacer
    elements.append(Spacer(1, 12))

    # Add the title
    title = Paragraph("HOTELZ ROOM BOOKED", styles['Title'])
    elements.append(title)

    # Add another spacer
    elements.append(Spacer(1, 12))

    # Draw booking details as paragraphs
    details = [
        f"<b>Username:</b> {booking.user.username}",
        f"<b>Booking ID:</b> {booking.booking_id}",
        f"<b>Amount Paid:</b> ₹{booking.amount}",
        f"<b>Room Type:</b> {booking.room.roomtype}",
        f"<b>Location:</b> {booking.room.location}",
        f"<b>From Date:</b> {booking.fromdate}",
        f"<b>To Date:</b> {booking.todate}",
        f"<b>Booked Date:</b> {booking.booked_on}",
    ]

    for detail in details:
        elements.append(Paragraph(detail, styles['Normal']))
        elements.append(Spacer(1, 12))  # Add space between lines

    # Add a thank you note
    thank_you = Paragraph("<i>Thank you for booking with us! We look forward to hosting you.</i>", styles['Italic'])
    elements.append(thank_you)

    # Build the PDF
    doc.build(elements)

    # Get the value of the BytesIO buffer and write it to the response.
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

def generate_ticket_pdf(booking):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()

    # Add the "BOOKED" image to the PDF
    img_path = "static/assets2/img/BOOKED-removebg-preview.png"  # Update the path to your image
    booked_img = Image(img_path, 2.5 * inch, 2.5 * inch)
    booked_img.hAlign = 'RIGHT'
    elements.append(booked_img)

    # Add a spacer
    elements.append(Spacer(1, 12))

    # Add the title
    title = Paragraph("HOTELZ ROOM BOOKED", styles['Title'])
    elements.append(title)

    # Add another spacer
    elements.append(Spacer(1, 12))

    # Draw booking details as paragraphs
    details = [
        f"<b>Username:</b> {booking.user.username}",
        f"<b>Booking ID:</b> {booking.booking_id}",
        f"<b>Amount Paid:</b> ₹{booking.amount}",
        f"<b>Room Type:</b> {booking.room.roomtype}",
        f"<b>Location:</b> {booking.room.location}",
        f"<b>From Date:</b> {booking.fromdate}",
        f"<b>To Date:</b> {booking.todate}",
        f"<b>Booked Date:</b> {booking.booked_on}",
    ]

    for detail in details:
        elements.append(Paragraph(detail, styles['Normal']))
        elements.append(Spacer(1, 12))  # Add space between lines

    # Add a thank you note
    thank_you = Paragraph("<i>Thank you for booking with us! We look forward to hosting you.</i>", styles['Italic'])
    elements.append(thank_you)

    # Build the PDF
    doc.build(elements)

    # Move the buffer pointer to the beginning
    buffer.seek(0)

    return buffer

# views.py
from django.shortcuts import render
from django.http import JsonResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@csrf_exempt
def new_order(request):
    if request.method == "POST":
        amount = int(request.POST['price']) * 100  # Convert to paise
        product_name = request.POST['product_name']

        new_order_response = razorpay_client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1"
        })

        response_data = {
            "callback_url": "http://127.0.0.1:8000/payment/callback",
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "order": new_order_response,
            "product_name": product_name
        }

        return JsonResponse(response_data)


@csrf_exempt
def order_callback(request):
    if request.method == "POST":
        try:
            razorpay_signature = request.POST.get("razorpay_signature")
            payment_id = request.POST.get("razorpay_payment_id")
            order_id = request.POST.get("razorpay_order_id")

            payment_verification = razorpay_client.utility.verify_payment_signature({
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': razorpay_signature
            })

            if payment_verification:
                return paymentsuccesspage(request)  #

            else:
                # Logic for failed verification
                return JsonResponse({"res": "failed"})
        except Exception as e:
            return JsonResponse({"res": "error", "message": str(e)})

@login_required()
def changepassword(request):
    if request.method == "POST":
        oldpassword = request.POST.get("oldpassword")
        newpassword = request.POST.get("newpassword")
        cpassword = request.POST.get("cpassword")
        user = request.user
        password_matched = check_password(oldpassword,request.user.password)
        special_characters = {'[', ']', '{', '}', '(', ')', '/', '?', '.', ',', ';', ':', '|', '*', '~', '`',
                              '!', '^', '-', '_', '+', '<', '>', '@', '#', '$', '%', '&'}
        if password_matched:
         if newpassword == cpassword and oldpassword != newpassword:
            if len(newpassword) < 8:
                messages.warning(request, "Password should be at least 8 characters")
                return redirect('changepassword')

            if not any(char in special_characters for char in newpassword):

                messages.warning(request, "Password should contain at least one special character.")
                return redirect('changepassword')

            user.set_password(newpassword)
            user.save()
            # It's a good practice to update the session hash after changing the password
            update_session_auth_hash(request, user)

            messages.warning(request,"Successfully Changed")
            redirect('changepassword')
         else:

           messages.warning(request,"Unsuccessful check your inputs.")
           redirect('changepassword')
        else:
            messages.warning(request, "Old password not matched")
            redirect('changepassword')
    return render(request, "changepassword.html",{'username' : request.user.username})



from django.shortcuts import render, redirect
from .forms import FeedbackForm
from .models import Feedback  # Make sure to import your model

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)  # Create the Feedback object but don't save it yet
            feedback.user_name = request.user.username  # Automatically set the username
            feedback.save()  # Save the feedback to the database
            return redirect('home')  # Redirect to a success page
    else:
        form = FeedbackForm()

    # Fetch existing feedback for display
    feedback_list = Feedback.objects.all()
    return render(request, 'feedback.html', {'form': form, 'feedback_list': feedback_list})

from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import MyBookings  # Adjust the import according to your models



def mybookings(request):
    # Retrieve all bookings for the current user
    my_bookings = MyBookings.objects.filter(user=request.user)
    bank_details = BankDetails.objects.filter(user=request.user, is_submitted=True).first()

    # Pass the current date and bank details submission status
    return render(request, "MyBookings.html", {
        "my_bookings": my_bookings,
        "today": timezone.now().date(),
        "bank_details_status": bank_details.is_submitted if bank_details else False  # Ensure it's a boolean
    })

from .models import BankDetails,ReturnAmount
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from .models import MyBookings, BankDetails, ReturnAmount
from django.conf import settings
from decimal import Decimal

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(MyBookings, id=booking_id, user=request.user)

    if booking.status == "Canceled":
        messages.warning(request, "This booking has already been canceled.")
    else:
        if booking.fromdate < timezone.now().date():
            messages.warning(request, "You cannot cancel this booking as the check-in date has passed.")
        else:
            # Cancel the booking
            booking.status = "Canceled"
            booking.save()
            messages.success(request, "Your booking has been successfully canceled.")

            # Retrieve bank details from BankDetails model
            bank_details = BankDetails.objects.filter(user=request.user, is_submitted=True).first()

            # Check if bank details exist before creating ReturnAmount
            if bank_details:
                try:
                   refund = ReturnAmount.objects.create(
                        user=request.user,
                        booking=booking,
                        account_holder_name=bank_details.account_holder_name,
                        bank_name=bank_details.bank_name,
                        account_number=bank_details.account_number,
                        ifsc_code=bank_details.ifsc_code,
                        email=bank_details.email,
                        phone_number=bank_details.phone_number,
                        refund_amount=booking.amount * Decimal('0.8'),
                        return_status=False  # Set return_status to False by default
                    )
                except Exception as e:
                    messages.error(request, f"Failed to create ReturnAmount record: {e}")
            else:
                messages.warning(request, "Bank details not found. Please add your bank details.")

            # Send email notification
            subject = "Booking Cancellation Confirmation"
            message = (
                f"Dear {booking.user.username},\n\n"
                f"Your booking with Booking ID {booking.booking_id} has been successfully canceled.\n"
                f"You will receive 80% of the amount {refund.refund_amount} paid back to your account within 3 working days.\n\n"
                "Thank you for choosing our service.\n\nBest regards,\nHotelz Team"
            )
            recipient_email = booking.user.email

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [recipient_email],
                fail_silently=False,
            )

    return redirect('mybookings')


# Redirect to the bookings page or another page





@login_required
def paymentreturn(request):
    # Check if the user has already submitted their payment return details
    if BankDetails.objects.filter(user=request.user, is_submitted=True).exists():
        messages.success(request, "You have already submitted your payment return details.")
        return redirect('mybookings')

    if request.method == 'POST':
        # Create a new BankDetails instance from POST data
        bank_details = BankDetails(
            user=request.user,
            account_holder_name=request.POST['account_holder_name'],
            bank_name=request.POST['bank_name'],
            account_number=request.POST['account_number'],
            ifsc_code=request.POST['ifsc_code'],
            email=request.POST['email'],
            phone_number=request.POST['phone_number'],
            is_submitted=True
        )
        bank_details.save()
        messages.success(request, "Payment return details submitted successfully.")
        return redirect('mybookings')

    return render(request, "paymentreturningform.html")

