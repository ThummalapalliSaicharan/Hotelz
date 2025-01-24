from django.contrib import admin
from django.urls import path
from . import views
from .views import  download_ticket

urlpatterns = [
  path('',views.index,name="index"),
  path('login',views.loginpage,name="loginpage"),
  path('register',views.register,name="register"),
 path('about',views.about,name="about"),
path('service',views.service,name="service"),
path('contact',views.contact,name="contact"),
    path('rooms',views.rooms,name="rooms"),
    path('home',views.home,name="home"),
    path('activate/<uidb64>/<token>', views.ActivateAccountView.as_view(), name="activate"),


    path('locationdelhi',views.delhi,name="delhi"),
    path('locationvijayawada',views.vijayawada,name="vijayawada"),
    path('locationkolkata', views.kolkata, name="kolkata"),
    path('locationhyderabad', views.hyderabad, name="hyderabad"),
    path('locationmumbai', views.mumbai, name="mumbai"),
    path('locationchennai', views.chennai, name="chennai"),
    path('locationpune', views.pune, name="pune"),
    path('locationbangalore', views.bangalore, name="bangalore"),
    path('locationlucknow', views.lucknow, name="lucknow"),
    path('locationamaravati', views.amaravati, name="amaravati"),
    path('locationahmedabad', views.ahmedabad, name="ahmedabad"),
    path('locationthiruvananthapuram', views.thiruvananthapuram, name="thiruvananthapuram"),

    path('hotelzreception', views.hotelzreception, name="hotelzreception"),
    path('roombooking', views.roombooking, name="roombooking"),
    path('roominformation', views.roominformation, name="roominformation"),
    path('payment', views.payment, name="payment"),
    path('paymentsuccesspage', views.paymentsuccesspage, name="paymentsuccesspage"),
    path('mybookings',views.mybookings,name="mybookings"),

    path('download_ticket/<int:booking_id>/', download_ticket, name='download_ticket'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),

    path('changepassword',views.changepassword,name='changepassword'),


    path('paymentreturningform',views.paymentreturn,name="paymentreturningform"),
    path('payment_call/', views.payment_call, name='payment_call'),
    path('payment/new-order', views.new_order, name='new_order'),
    path('payment/callback', views.order_callback, name='order_callback'),

    path('logout/', views.logoutpage, name='logout'),
]
