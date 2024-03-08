from django.urls import path 
from .import views  

urlpatterns = [

    path("",views.Index,name="Index"),
    path("SignUp",views.SignUp,name="SignUp"),
    path("SignIn",views.SignIn,name="SignIn"),
    path("SignOut",views.SignOut,name="SignOut"),
    path("BookingConfirm",views.BookingConfirm,name="BookingConfirm"),
    path("DeleteHotel/<int:pk>",views.DeleteHotel,name="DeleteHotel"),
    path("HotelAdd",views.HotelAdd,name="HotelAdd"),
    path("CustomerBookings",views.CustomerBookings,name="CustomerBookings"),
    path("AdminHome",views.AdminHome,name="AdminHome"),
    path("BookHotel/<int:pk>",views.BookHotel,name="BookHotel"),
    path("ProceedCheckout/<int:pk>",views.ProceedCheckout,name="ProceedCheckout"),
    path("Mybookings",views.Mybookings,name="Mybookings"),
    path("Rooms",views.Rooms,name="Rooms"),
    path("Contact",views.Contact,name="Contact"),
    path("deleteHotelBooking/<int:pk>",views.deleteHotelBooking,name="deleteHotelBooking"),
    path("BlockRoom/<int:pk>",views.BlockRoom,name="BlockRoom"),
    path("UnBlockRoom/<int:pk>",views.UnBlockRoom,name="UnBlockRoom"),
    path("SuperAdmin",views.SuperAdmin,name="SuperAdmin"),


]