from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login,logout
from .forms import UserAddForm, HotelAddForm
from django.contrib.auth.models import User,Group
from .decorators import admin_only
from django.contrib.auth.decorators import login_required
from .models import Hotels, HotelBooking

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest

# Create your views here.
# Authetication functions 

razorpay_client = razorpay.Client(
  auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@admin_only
def Index(request):
    hotels = Hotels.objects.all()

    context = {
        "hotels":hotels
    }
    return render(request,"index.html",context)

def AdminHome(request):
    return render(request,"adminindex.html")

def SignIn(request):
    if request.method == "POST":
        username = request.POST['uname']
        password = request.POST['pswd']
        user1 = authenticate(request, username = username , password = password)
        
        if user1 is not None:
            
            request.session['username'] = username
            request.session['password'] = password
            login(request, user1)
            return redirect('Index')
        
        else:
            messages.info(request,'Username or Password Incorrect')
            return redirect('SignIn')
    return render(request,"login.html")

def SignUp(request):
    form = UserAddForm()
    if request.method == "POST":
        fname = request.POST["fname"]
        email = request.POST["email"]
        uname = request.POST["uname"]
        pswd = request.POST["pswd"]
        pswd1 = request.POST["pswd1"]

        if pswd != pswd1:
            messages.info(request,"Password Do not Matches..")
            return redirect("SignUp")
        if User.objects.filter(username = uname).exists():
            messages.info(request,"Username alredy exists user another username")
            return redirect("SignUp")
        if User.objects.filter(email = email).exists():
            messages.info(request,"Email alredy exists user another email")
            return redirect("SignUp")
        else:
            user = User.objects.create_user(first_name=fname, email=email, username=uname, password = pswd)
            user.save()
            messages.success(request,"User Created.. Please Login....")
            return redirect("SignIn")




        # form = UserAddForm(request.POST)
        # if form.is_valid():
        #     username = form.cleaned_data.get('username')
        #     email = form.cleaned_data.get("email")
        #     if User.objects.filter(username = username).exists():
        #         messages.info(request,"Username Exists")
        #         return redirect('SignUp')
        #     if User.objects.filter(email = email).exists():
        #         messages.info(request,"Email Exists")
        #         return redirect('SignUp')
        #     else:
        #         new_user = form.save()
        #         new_user.save()
                
                # group = Group.objects.get(name='user')
                # new_user.groups.add(group) 
                
                
            
    return render(request,"register.html",{"form":form})



def SignOut(request):
    logout(request)
    return redirect('Index')

# Hotel Add

@login_required(login_url="SignIn")
def HotelAdd(request):
    form = HotelAddForm()
    hotel = Hotels.objects.filter(user = request.user)
    if request.method == "POST":
        form = HotelAddForm(request.POST,request.FILES)
        if form.is_valid():
            hotel = form.save()
            hotel.user = request.user
            hotel.save()
            messages.info(request,"Hotel Addedd")
            return redirect("HotelAdd")
    context = {
        "form":form,
        "hotel":hotel
    }
    return render(request,"addrooms.html",context)


def DeleteHotel(request,pk):
    Hotels.objects.get(id = pk).delete()
    messages.info(request,"Hotel Deleted")

    return redirect("HotelAdd")



# bookings 
@login_required(login_url="SignIn")
def BookHotel(request,pk):
    room = Hotels.objects.get(id = pk)
    if request.method == "POST":
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']
        req = request.POST['requests']
        date = request.POST["sdate"]
        cdate = request.POST["cdate"]
        booking = HotelBooking.objects.create(Hotel = room,user = request.user,booker_Name = name, booker_phone = phone, booker_address = address, booking_date = date,special_Requests =req, status = "Hotel Booked" )
        booking.save()
        messages.info(request, "Hotel Booked")
        return redirect("ProceedCheckout",pk = booking.id)


    context = {
        "room":room
    }
    return render(request,"booking.html",context)

# paymet

@login_required(login_url='SignIn')
def ProceedCheckout(request,pk):
    Hotel = HotelBooking.objects.get(id = pk)
   
    currency = 'INR'
    amount = Hotel.Hotel.Price * 100 # Rs. 200
    context = {}

  # Create a Razorpay Order Pyament Integration.....
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                          currency=currency,
                          payment_capture='0'))

  # order id of newly created order.
    razorpay_order_id = razorpay_order["id"]
    callback_url = "paymenthandler/"

  # we need to pass these details to frontend.
    
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url 
    context['slotid'] = "1",
    context['total'] = Hotel.Hotel.Price
    # context['amt'] = (product1.Product_price)*float(qty)
    
    return render(request,'checkoutpage.html',context)


@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

      # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
           
            try:
                print("working 1")
                razorpay_client.payment.capture(payment_id, 800)
                return redirect('Success1')
        # render success page on successful caputre of payment
            except:
                print("working 2")
                return redirect('Success1')
                    
                    
          # if there is an error while capturing payment.
            else:
                return render(request, 'paymentfail.html')
        # if signature verification fails.    
        except:
            return HttpResponseBadRequest()
        
      # if we don't find the required parameters in POST data
    else:
  # if other than POST request is made.
        return HttpResponseBadRequest()
    
def Success1(request):
    return render(request,'Paymentconfirm.html')



def BookingConfirm(request):
    return render(request, "bookingconfirm.html")


def HotelSearch(request):
    if request.method == "POST":
        start = request.POST["start"]
        end = request.POST["end"]

        journy = Hotels.objects.filter(staring_from__contains = start, destination__contains = end).order_by("Time_Taken_toTravel_in_Hours")

        context = {
            "journy":journy
        }
        return render(request,"search2.html",context)

    return render(request,"search2.html")

def CustomerBookings(request):
    hotel = HotelBooking.objects.filter(Hotel__user = request.user)
    context = {
        "hotel":hotel,
        
    }
    return render(request,"customerbooking.html",context)

def deleteHotelBooking(request,pk):
    HotelBooking.objects.get(id = pk).delete()
    return redirect("Index")



@login_required(login_url="SignIn")
def Mybookings(request):
    hotel = HotelBooking.objects.filter(user = request.user)
   

    context = {
        "hotel":hotel,
        
    }

    return render(request, "mybookings.html",context)


def Rooms(request):
    room = Hotels.objects.all()
    context  = {
        "room":room
    }
    return render(request,"rooms.html",context)

def Contact(request):
    return render(request,"contact.html")

def BlockRoom(request,pk):
    hot = Hotels.objects.get(id= pk)
    hot.availability = False
    hot.save()
    messages.info(request,"Status Changed.....")
    return redirect("HotelAdd")

def UnBlockRoom(request,pk):
    hot = Hotels.objects.get(id= pk)
    hot.availability = True
    hot.save()
    messages.info(request,"Status Changed.....")
    return redirect("HotelAdd")


def SuperAdmin(request):
    if request.method == "POST":
        fname = request.POST["fname"]
        email = request.POST["email"]
        uname = request.POST["uname"]
        pswd = request.POST["pswd"]
        pswd1 = request.POST["pswd1"]

        if pswd != pswd1:
            messages.info(request,"Password Do not Matches..")
            return redirect("SuperAdmin")
        if User.objects.filter(username = uname).exists():
            messages.info(request,"Username alredy exists user another username")
            return redirect("SuperAdmin")
        if User.objects.filter(email = email).exists():
            messages.info(request,"Email alredy exists user another email")
            return redirect("SuperAdmin")
        else:
            user = User.objects.create_user(first_name=fname, email=email, username=uname, password = pswd)
            user.save()
            group = Group.objects.get(name='staff')
            user.groups.add(group) 
            messages.success(request,"User Created.. Please Login....")
            return redirect("SuperAdmin")
        
    return render(request,"superadmin.html")