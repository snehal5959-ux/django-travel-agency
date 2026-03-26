from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .models import Feedback, TravelPackage, Favourite, Country, Place
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Booking
from django.shortcuts import get_object_or_404
import datetime
from django.http import HttpResponse
from django.contrib import messages

from .models import (
    TravelPackage,
    Booking,
    Blog,
    Country,
    Feedback,
    ContactMessage
)

from decimal import Decimal
# from datetime import datetime
from django.utils import timezone
from django.utils.timezone import now
from decimal import Decimal

from .models import TravelPackage, Booking, UserProfile
from .utils import validate_booking, calculate_total_price, generate_flouci_payment
from .models import Blog, History
from django.db.models import Q
import razorpay
from django.conf import settings
from django.http import JsonResponse
from .forms import UserUpdateForm, ProfileUpdateForm
# views.py
from datetime import date
from packages.models import InboxMessage

from django.utils import timezone
from django.contrib import messages
from decimal import Decimal


@login_required
def request_refund(request, pk):
    booking = get_object_or_404(Booking, id=pk)

    booking.refund_requested = True
    booking.save()

    return redirect("cancel_booking", booking_id=pk)

@login_required
def user_inbox(request):
    messages = InboxMessage.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(request, "user_inbox.html", {
        "messages": messages
    })


def reset_password(request):
    if request.method == "POST":
        username = request.POST.get("username")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect("reset_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("reset_password")

        user.set_password(new_password)
        user.save()

        messages.success(request, "Password reset successfully. Please login.")
        return redirect("login")

    return render(request, "reset_password.html")

@login_required
def inbox_message_detail(request, message_id):
    message = get_object_or_404(
        InboxMessage,
        id=message_id,
        user=request.user
    )

    # Mark as read
    if not message.is_read:
        message.is_read = True
        message.save()

    return render(request, "message_detail.html", {
        "message": message
    })

#compose


@login_required
def account_settings(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()

            messages.success(request, "Profile updated successfully!")

            return redirect('profile')   # 🔹 Redirect after saving

    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=profile)

    context = {
        "u_form": u_form,
        "p_form": p_form
    }

    return render(request, "account_settings.html", context)


def create_order(request):
    data = json.loads(request.body)
    amount = int(float(data["amount"]) * 100)  # convert to paise

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return JsonResponse({
        "order_id": order["id"],
        "amount": order["amount"],
        "key": settings.RAZORPAY_KEY_ID
    })



# ADMIN – LIST ALL PACKAGES
@login_required
def admin_package_list(request):
    packages = TravelPackage.objects.all().order_by('-id')
    return render(request, 'package_list.html', {
        'packages': packages
    })


# ADMIN – ADD NEW PACKAGE
@login_required
def admin_add_package(request):
    if request.method == 'POST':
        form = TravelPackageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_package_list')
    else:
        form = TravelPackageForm()

    return render(request, 'package_form.html', {
        'form': form,
        'title': 'Add New Package'
    })



# ADMIN – DELETE PACKAGE
@login_required
def admin_delete_package(request, pk):
    package = get_object_or_404(TravelPackage, pk=pk)

    if request.method == 'POST':
        package.delete()
        return redirect('admin_package_list')

    return render(request, 'package_confirm_delete.html', {
        'package': package
    })



@login_required
def profile(request):
    user = request.user  # Django User object

    profile, created = UserProfile.objects.get_or_create(user=request.user)

    context = {
        'user': user,
        'profile': profile,
    }
    return render(request, 'profile.html', context)


def search_packages(request):
    query = request.GET.get('q', '').strip()

    if not query:
        return redirect('travel_package_list')

    packages = TravelPackage.objects.filter(
        Q(destination__icontains=query) |
        Q(name__icontains=query)
    )

    # If only ONE package found → redirect to booking page
    if packages.count() == 1:
        return redirect('booking_handler_view', package_id=packages.first().id)

    # If MULTIPLE packages → show filtered package list
    return render(request, 'package_list.html', {
        'packages': packages,
        'search_query': query
    })


# --------------------- HOME ---------------------
def home(request):
    packages = TravelPackage.objects.all()
    countries = Country.objects.all()
    ratings_range = range(1, 6)

    return render(request, 'travel_package_list.html', {
        'packages': packages,
        'ratings_range': ratings_range,
        'countries': countries
    })



# --------------------- REGISTER ---------------------
def register(request):
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        password = request.POST.get('password', '').strip()
        confirm = request.POST.get('confirm', '').strip()

        if not all([name, email, phone, password, confirm]):
            messages.error(request, "All fields are required")
            return redirect('register')

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return redirect('register')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        UserProfile.objects.create(user=user, phone=phone)

        messages.success(request, "Registration successful 🎉 Please login")
        return redirect('login')

    return render(request, 'register.html')


# --------------------- LOGIN ---------------------
def login(request):
    if request.method == "POST":
     if request.method == "POST":
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()

        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successful 🎉")
            return redirect('home')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('login')

    return render(request, 'login.html')
# --------------------- LOGOUT ---------------------
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login')


# --------------------- CONTACT ---------------------
@login_required
def contact(request):
    success = False

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if name and email and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message
            )
            success = True

    return render(request, "contact.html", {"success": success})


# --------------------- PACKAGE LIST ---------------------
def travel_package_list(request):
    packages = TravelPackage.objects.all()
    ratings_range = range(1, 6)
    return render(request, 'travel_package_list.html', {
        'packages': packages,
        'ratings_range': ratings_range
    })


# --------------------- BOOK PACKAGE ---------------------
@login_required
def book_package(request, pk):
    package = get_object_or_404(TravelPackage, pk=pk)
    return render(request, 'travel_package_booking.html', {'package': package})


# --------------------- BOOKING HANDLER ---------------------
@login_required
def debug_booking(request, package_id):
    from decimal import Decimal
    package = get_object_or_404(TravelPackage, id=package_id)

    if request.method == "POST":
        print("POST DATA:", request.POST)
        try:
            # Convert to proper types
            num_adults = int(request.POST.get("SelectPerson", "0") or 0)
            num_children = int(request.POST.get("SelectKids", "0") or 0)
            booking_date = request.POST.get("datetime", "").strip()

            if not booking_date:
                raise ValueError("Booking date is required.")

            booking = Booking.objects.create(
                user=request.user,
                package=package,
                name=request.POST.get("name", "").strip(),
                email=request.POST.get("email", "").strip(),
                gender=request.POST.get("SelectGender", "None"),
                datetime=booking_date,   # must be a valid datetime string
                num_adults=num_adults,
                num_children=num_children,
                payment_method=request.POST.get("payment_method", "").strip(),
                payment_status="Pending",
                total_price=Decimal(package.price),
            )
            print("Booking created with ID:", booking.id)
            return render(request, "booking_success.html", {"booking": booking})
        except Exception as e:
            import traceback
            traceback.print_exc()
            return render(request, "booking_fail.html", {"error": str(e)})

    return render(request, "travel_package_booking.html", {"package": package})


@login_required
def compose_message(request):
    users = User.objects.all()

    if request.method == "POST":
        user_id = request.POST.get("user_id")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        user = User.objects.filter(id=user_id).first()

        if user:
            InboxMessage.objects.create(
                user=user,
                subject=subject,
                message=message
            )


    return render(request, "compose_message_all.html", {
        "users": users
    })

@login_required
def booking_handler_view(request, package_id):
    package = get_object_or_404(TravelPackage, id=package_id)

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        datetime_value = request.POST.get("datetime")
        gender = request.POST.get("SelectGender")
        address = request.POST.get("address")
        num_adults = int(request.POST.get("SelectPerson"))
        num_children = int(request.POST.get("SelectKids"))
        payment_method = request.POST.get("payment_method")

        total_price = (
            num_adults * package.price
        ) + (num_children * package.price * Decimal("0.5"))

        booking = Booking.objects.create(
            user=request.user,
            package=package,
            name=name,
            email=email,
            address=address,
            gender=gender,
            datetime=datetime_value,
            num_adults=num_adults,
            num_children=num_children,
            payment_method=payment_method,
            total_price=total_price,
            payment_status="Pending",
            booking_status="Pending",
        )

        # ✅ If On Site → direct success
        if payment_method == "On Site":
            return redirect("booking_success")

        # ✅ If Online → return booking id to JS
        return JsonResponse({
            "booking_id": booking.id,
            "total_price": float(total_price)
        })

    return render(request, "travel_package_booking.html", {
        "package": package
    })


@login_required
def payment_page(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, "payment_page.html", {"booking": booking})


@csrf_exempt
@login_required
def create_razorpay_order(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request"}, status=400)

    try:
        import json
        data = json.loads(request.body)

        amount = data.get("amount")
        if not amount:
            return JsonResponse({"error": "Amount required"}, status=400)

        amount = int(amount)  # already in paise

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": 1
        })

        return JsonResponse({
            "key": settings.RAZORPAY_KEY_ID,
            "order_id": order["id"],
            "amount": order["amount"]
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)



@login_required
def payment_success(request, booking_id):

    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    print("VIEW HIT")
    print("METHOD:", request.method)

    if request.method == "POST":

        booking.email = request.POST.get("email")
        booking.transaction_id = request.POST.get("transaction_id")
        booking.payment_screenshot = request.POST.get("payment_screenshot")

        booking.payment_status = "Paid"
        booking.booking_status = "Confirmed"

        booking.save()

        return render(request, "booking_success.html", {
            "booking": booking
        })

    return render(request, "payment_success.html", {
        "booking": booking
    })



@csrf_exempt
@login_required
def submit_booking(request, package_id):
    if request.method != "POST":
        return JsonResponse({"success": False}, status=400)

    try:
        data = json.loads(request.body)

        booking = Booking.objects.create(
            user=request.user,                    # ✅ REQUIRED
            package_id=package_id,                # ✅ REQUIRED
            name=data["name"],                    # ✅ REQUIRED
            email=data["email"],                  # ✅ REQUIRED
            gender=data.get("gender", "None"),
            datetime=data["datetime"],             # ✅ REQUIRED
            num_adults=data.get("num_adults", 1),
            num_children=data.get("num_children", 0),
            payment_method=data.get("payment_method", "Online"),
            payment_status="Pending",              # ✅ MANUAL FLOW
            booking_status="Pending",
            total_price=data["total_price"],       # ✅ REQUIRED
        )

        return JsonResponse({
            "success": True,
            "booking_id": booking.id
        })

    except Exception as e:
        print("BOOKING ERROR 👉", e)
        return JsonResponse({"success": False})




@login_required
def booking_success(request):
    booking = Booking.objects.filter(user=request.user).order_by('-created_at').first()
    return render(request, "booking_success.html", {"booking": booking})




# --------------------- BOOKING FAIL ---------------------
def booking_fail(request):
    messages.error(request, "Booking failed. Please try again.")
    return render(request, "booking_fail.html")

# --------------------- RECOMMENDATIONS ---------------------
def packages_recommendations(request):
    packages = TravelPackage.objects.filter(available=True)
    price = request.GET.get('price')
    category = request.GET.get('category')

    if price == 'low':
        packages = packages.filter(price__lt=10000)
    elif price == 'medium':
        packages = packages.filter(price__gte=10000, price__lte=30000)
    elif price == 'high':
        packages = packages.filter(price__gt=30000)

    if category:
        packages = packages.filter(package_type=category)

    return render(request, 'recommendations.html', {
        'packages': packages,
        'selected_price': price,
        'selected_category': category,
    })

#chatbot
# --------------------- STATIC PAGES ---------------------
def blog(request):
    blogs = Blog.objects.all().order_by('-date')   # IMPORTANT
    return render(request, 'blog.html', {'blogs': blogs})


def terms(request):
    return render(request, 'terms.html')


def privacy(request):
    return render(request, 'privacy.html')


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, 'blog_detail.html', {'blog': blog})


def blog_detail(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, 'blog_detail.html', {'blog': blog})

def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blog.html', {'blogs': blogs})


@login_required
def feedback_view(request):
    packages = TravelPackage.objects.all()  # For dropdown selection

    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        package_id = request.POST.get('package')
        message = request.POST.get('message', '').strip()
        rating = int(request.POST.get('rating', 5))

        if not name or not message or not rating:
            messages.error(request, "Please fill in all required fields.")
            return redirect('feedback')

        package = TravelPackage.objects.filter(id=package_id).first() if package_id else None

        Feedback.objects.create(
            user=request.user,
            name=name,
            package=package,
            message=message,
            rating=rating
        )

        messages.success(request, "Thank you for your feedback!")
        return redirect('home')

    return render(request, 'feedback.html', {'packages': packages})


@login_required
def booking_history_view(request):
    bookings = Booking.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(request, 'history.html', {
        'bookings': bookings
    })


@login_required
def cancel_booking_view(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user
    )

    if booking.payment_status != 'Cancelled':
        booking.payment_status = 'Cancelled'
        booking.save()
        messages.warning(request, 'Booking cancelled.')

    return redirect('history')



def add_to_favourites(request, package_id):
    package = get_object_or_404(TravelPackage, id=package_id)
    fav, created = Favourite.objects.get_or_create(user=request.user, package=package)
    if created:
        messages.success(request, "Added to favourites ❤️")
    else:
        messages.info(request, "Already in favourites")
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def remove_from_favourites(request, package_id):
    fav = Favourite.objects.filter(user=request.user, package_id=package_id)
    if fav.exists():
        fav.delete()
        messages.success(request, "Removed from favourites ❌")
    else:
        messages.info(request, "Not in favourites")
    return redirect('favourites_list')


def favourites_list(request):
    fav_packages = Favourite.objects.filter(user=request.user)
    return render(request, 'favourites.html', {'fav_packages': fav_packages})

def travel_package_list(request):
    packages = TravelPackage.objects.all()
    ratings_range = range(1, 6)
    return render(request, 'travel_package_list.html', {
        'packages': packages,
        'ratings_range': ratings_range
    })

def travel_package_detail(request, package_id):
    """
    Displays the details of a single travel package in a card or page format.
    """
    package = get_object_or_404(TravelPackage, id=package_id)
    ratings_range = range(1, 6)  # For star rating display

    context = {
        'package': package,
        'ratings_range': ratings_range
    }

    return render(request, 'details.html', context)

def travel_news_list(request):
    return render(request, 'travel_news_list.html')

def countries(request):
    return render(request, 'countries.html', {
        'countries': Country.objects.all()
    })


def country_places(request, country_name):
  country = get_object_or_404(Country, name=country_name)
  places = [
    {
        "name": country.place1_name,
        "image": country.place1_image,
        "description": country.place1_description
    },
    {
        "name": country.place2_name,
        "image": country.place2_image,
        "description": country.place2_description
    },
    {
        "name": country.place3_name,
        "image": country.place3_image,
        "description": country.place3_description
    },
    {
        "name": country.place4_name,
        "image": country.place4_image,
        "description": country.place4_description
    },
]
  places = [p for p in places if p["name"]]
  return render(request, 'country_places.html', {
        'country': country,
        'places': places
    })

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == "POST":
        booking.payment_status = "Cancelled"
        booking.cancel_reason = request.POST.get('cancel_reason')
        booking.cancelled_at = timezone.now()
        booking.save()


        messages.success(request, "Booking cancelled successfully.")
        return redirect('booking_history_view')

    return render(request, 'booking_cancel.html', {'booking': booking})

@login_required
def refund_booking(request, booking_id):
    booking = get_object_or_404(
        Booking,
        id=booking_id,
        user=request.user,
        refund_status='Pending'
    )

    

    booking.refund_status = 'Refunded'
    booking.refunded_at = timezone.now()
    booking.save()

    messages.success(request, "Refund processed successfully 💸")
    return redirect('booking_history_view')


def invoice_view(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    # Calculate children discount (50%)
    children_total = booking.package.price * booking.num_children
    discount = children_total * Decimal(0.5)

    context = {
        "booking": booking,
        "today": now().date(),
        "discount": discount,
    }

    return render(request, "invoice.html", context)


def invoice_pdf(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    template = get_template('invoice_pdf.html')  # same template
    context = {
        'booking': booking,
        'today': datetime.date.today(),
        'discount': 0,
    }

    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (f'attachment; filename="invoice_{booking.id}.pdf"')

    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("Error generating PDF")

    return response