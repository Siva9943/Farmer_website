from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
# from django.utils.translation import gettext as 
from django.contrib.auth.models import User
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from allauth.socialaccount.models import SocialAccount
from .forms import *
from .models import *

def home(request):
    return render(request, 'index.html',{'active_page': 'index'})

# signup
def signup(request):
    form=CustomUserForm()
    if request.method == 'POST':
        form=CustomUserForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            email = request.POST.get('email')
            role = request.POST.get('role')
            username = request.POST.get('username')
            district = request.POST.get('district')

            user_info = User.objects.filter(email=email).first()

            # Save user details
            User_Details.objects.create(
                user=user_info,
                username=username,
                email=email,
                district=district,
                role=role
            )
            print("User details saved.")

            # Save seller details if applicable
            if role == 'seller':
                Seller.objects.create(
                    user=user_info,
                    name=username,
                    mobile_number=request.POST.get('mobile_number'),
                    latitude=float(request.POST.get('latitude', 0)),
                    longitude=float(request.POST.get('longitude', 0)),
                    flat_details=request.POST.get('flat_details'),
                    area_details=request.POST.get('area_details'),
                    landmark=request.POST.get('landmark'),
                    pincode=request.POST.get('pincode'),
                    district=district,
                    state=request.POST.get('state')
                )
                print("Seller details saved.")

            return redirect('login_info')
        else:
            print("error")
            return redirect('signup')
    return render(request, 'signup.html')

def seller_login(request):
    if request.method == 'POST':
        try:
            username_or_email = request.POST.get('username').strip()
            password = request.POST.get('password').strip()
            user = authenticate(request, username=username_or_email, password=password)
            if user is None:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None
            if user is not None:
                login(request, user)
                return redirect('seller_dashboard')
            else:
                messages.error(request, "Invalid credentials")
        except Exception as e:
            print("Login error:", e)
    return render(request, 'seller_login.html')
#  login 
from urllib.parse import urlencode

def login_form(request):
    if request.method == 'POST':
        try:
            username_or_email = request.POST.get('username').strip()
            password = request.POST.get('password').strip()
            user = authenticate(request, username=username_or_email, password=password)
            if user is None:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None
            if user is not None:
                try:
                    if user.is_superuser:  
                        login(request, user)
                        return redirect('admin/')
                    else:
                        params = urlencode({'error': 'empty'})
                        return redirect(f"/login/?{params}")
                except Exception as e:
                    print("Login error:", e)
            else:
                params = urlencode({'error': 'invalid'})
                return redirect(f"/login/?{params}")
        except Exception as e1:
            print("Login error:", e1)
    return render(request, 'login.html')



# seller_dashboard
def seller(request):
    return render(request,'seller/seller_dashboard.html')
# loader page

def loader_view(request):
    return render(request, 'loader.html', {'redirect_url': '/'}) 

def form_submit(request):
    if request.method == 'POST':
        return redirect('loader')
    return render(request, 'form.html')
    # --------------------------------------


def market_price_view(request):
    prices = VegetableRate.objects.all().order_by('-id')
    return render(request, 'menu/market_price.html', {
        'prices': prices,
        'active_page': 'market_price'
    })


def buy_sell_view(request):
    products = Product.objects.select_related('seller').order_by('-posted_on')
    return render(request, 'e-com/buy_sell.html', {'products': products})
def farming_videos_view(request):
    videos = TipVideo.objects.all().order_by('-published_on')
    return render(request, 'social_media/farming_videos.html', {'videos': videos})
def government_schemes_view(request):
    schemes = Scheme.objects.all().order_by('-published_on')
    return render(request, 'govt/govt.html', {'schemes': schemes})

def weather_view(request):
    return render(request, 'menu/weather.html')

def news_view(request):
    news_items = News.objects.all().order_by('-published_on')
    return render(request, 'menu/news.html', {'news_items': news_items})

def community_view(request):
    posts = CommunityPost.objects.all().order_by('-created_at')
    return render(request, 'form/community.html', {'posts': posts})


def add_comment(request, post_id):
    if request.method == "POST":
        content = request.POST.get('comment')
        if content:
            Comment.objects.create(
                post_id=post_id,
                user=request.user,
                comment=content
            )
    return redirect('community')



# contact 
def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            
            send_mail(
                f"Farmer Guide Contact - {name}",
                message,
                email,
                ['your-email@example.com'],
            )
            
            messages.success(request, "Thank you for contacting us!")
            return redirect('contact')
    else:
        form = ContactForm()
    return render(request, 'form/contact.html', {'form': form})



def admin_login(request):
    return render(request,'admin/admin_dashboard.html')


def farmer_signup_view(request):
    soil_types = SoilType.objects.all()
    return render(request, 'farmer_signup.html', {'soil_types': soil_types})



# Create your views here.
@login_required(login_url='/login/')
def index(request):
    name=''
    picture=''
    if request.user.is_authenticated:
        try:
            account = SocialAccount.objects.get(user=request.user)
            name = account.extra_data.get('name', '')
            picture = account.extra_data.get('picture', '')
            print(name)
        except SocialAccount.DoesNotExist:
            pass 
    return render(request, 'index.html', {'name': name,'picture': picture
    })




# django-admin compilemessages
def my_view(request):
    message = _("Hello, world!")

# search input
def search_view(request):
    query = request.GET.get('q')
    return render(request, 'search_results.html', {'query': query})




def product_list(request):
    products = Seller.objects.all().order_by('-id')  
    return render(request, 'product_list.html', {'products': products})

def product_detail(request, seller_id):
    seller = get_object_or_404(Seller, pk=seller_id)
    farmer_profile = None
    try:
        farmer_profile = seller.user.farmer
    except Users.DoesNotExist:
        farmer_profile = None

    return render(request, 'product_detail.html', {
        'seller': seller,
        'farmer': farmer_profile
    })
# feedback

def feedback_view(request):
    if request.method == 'POST':
        print(request.POST)
        form = FeedbackForm(request.POST)
        print(1)
        if form.is_valid():
            print(2)
            form.save()
            messages.success(request, "Thank you for your message. We'll get back to you soon!")
            return redirect('contact')  
        else:
            form = FeedbackForm()
    return render(request, 'contact.html', {'form': form})


# admin dashboard
# crop upload
def crop_view(request):
    return render(request,'crop_guide.html')
def upload_crop(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            user_id =request.user.id
            data=Crop.objects.create(
                name=request.POST.get('name'),
                soil_type=request.POST.get('soil_type'),
                season=request.POST.get('season'),
                image=request.FILES['image'],
                # user_id-user_id,
                description=request.POST.get('description')
            )
            data.save()
            messages.success(request,"Crop upload successfully")
            return redirect('crop_view' )
        else:
            return redirect('upload_crop')
    return render(request,'admin/menu/upload_crop.html' ,{'active_page': 'crop_ac'})
def crop_view(request):
    crops = Crop.objects.all()
    crop_id = request.GET.get('id')
    crop = Crop.objects.filter(id=crop_id).first() if crop_id else None
    return render(request, 'admin/menu/view_crop.html', {
        'crops': crops,
        'crop': crop
    })





def market_price_view(request):
    prices = VegetableRate.objects.all().order_by('name')
    return render(request, 'menu/market_price.html', {'prices': prices})

# Vegitable rate
import openpyxl
from django.shortcuts import render, redirect
from .forms import ExcelUploadForm
from .models import VegetableRate

def vegitable_data(request):
    if request.method == 'POST':
        print("POST request received")
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            wb = openpyxl.load_workbook(file)
            sheet = wb.active

            for row in sheet.iter_rows(min_row=2, values_only=True):
                name, min_rate, max_rate = row
                if name and min_rate is not None and max_rate is not None:
                    VegetableRate.objects.create(
                        name=name.strip(),
                        min_rate=min_rate,
                        max_rate=max_rate
                    )
            return redirect('vegetable_data')  # or any success page
    else:
        print("else")
        prices = VegetableRate.objects.all().order_by('name')
        form = ExcelUploadForm()

    return render(request, 'admin/update_data/market_price_update.html', {'prices': prices, 'form': form, 'active_page': 'mark'})


# sms verification


from django.shortcuts import render, redirect
from .utils import send_otp

# def send_otp_view(request):
#     if request.method == 'POST':
#         form = MobileForm(request.POST)
#         if form.is_valid():
#             mobile = form.cleaned_data['mobile']
#             otp = send_otp(mobile)
#             MobileOTP.objects.update_or_create(mobile=mobile, defaults={'otp': otp})
#             request.session['mobile'] = mobile
#             return redirect('verify_otp')
#     else:
#         form = MobileForm()
#     return render(request, 'send_otp.html', {'form': form})


# def verify_otp_view(request):
#     mobile = request.session.get('mobile')
#     if not mobile:
#         return redirect('send_otp')
    
#     if request.method == 'POST':
#         form = OTPForm(request.POST)
#         if form.is_valid():
#             entered_otp = form.cleaned_data['otp']
#             obj = MobileOTP.objects.filter(mobile=mobile, otp=entered_otp).first()
#             if obj:
#                 return render(request, 'success.html', {'mobile': mobile})
#             else:
#                 return render(request, 'verify_otp.html', {'form': form, 'error': 'Invalid OTP'})
#     else:
#         form = OTPForm()
#     return render(request, 'verify_otp.html', {'form': form})




def logout_user(request):
    logout(request)  
    return redirect("/") 