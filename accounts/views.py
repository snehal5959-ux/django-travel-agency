from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from packages.models import TravelPackage, Feedback
from packages.models import Favourite, Country, Place

from accounts.forms import TravelPackageForm
from packages.models import Booking  
from django.contrib.auth.models import User  
from django.db.models import Sum
from django.shortcuts import render
from .forms import CountryForm, BlogForm, TravelNewsForm
from packages.models import Feedback
from packages.models import ContactMessage, InboxMessage
from .forms import AdminBookingUpdateForm
from news.models import TravelNews
from home.models import Gallery

def admin_gallery(request):

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        image = request.FILES.get("image")

        if title and image:
            Gallery.objects.create(
                title=title,
                description=description,
                image=image
            )
        return redirect("admin_gallery")

    gallery = Gallery.objects.all().order_by("-created_at")

    return render(request, "admin_gallery.html", {"gallery": gallery})

def admin_update_package(request, pk):
    package = get_object_or_404(TravelPackage, pk=pk)

    if request.method == "POST":
        form = TravelPackageForm(request.POST, request.FILES, instance=package)
        if form.is_valid():
            form.save()
            return redirect('admin_package_list')
    else:
        form = TravelPackageForm(instance=package)

    return render(request, "package_form.html", {
        "form": form,
        "title": "Update Travel Package"
    })


def delete_gallery(request, id):
    image = get_object_or_404(Gallery, id=id)
    image.delete()
    return redirect("admin_gallery")

def admin_news_list(request):
    news_list = TravelNews.objects.all().order_by('-published_date')  # latest first

    context = {
        'news_list': news_list
    }

    return render(request, 'admin_news_list.html', context)

@staff_member_required
def admin_refund_requests(request):
    bookings = Booking.objects.filter(refund_requested=True)

    return render(request, 'admin_refund_requests.html', {
        'bookings': bookings
    })

from packages.models import Blog
from news.models import TravelNews

# ADD NEWS
@staff_member_required
def admin_add_news(request):
    if request.method == "POST":
        form = TravelNewsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_news_list')
    else:
        form = TravelNewsForm()

    return render(request, 'admin_news_form.html', {
        'form': form,
        'title': 'Add New News'
    })


# UPDATE NEWS
@staff_member_required
def admin_update_news(request, pk):
    news = get_object_or_404(TravelNews, pk=pk)

    if request.method == "POST":
        form = TravelNewsForm(request.POST, instance=news)
        if form.is_valid():
            form.save()
            return redirect('admin_news_list')
    else:
        form = TravelNewsForm(instance=news)

    return render(request, 'admin_news_form.html', {
        'form': form,
        'title': 'Update News'
    })


# DELETE NEWS
@staff_member_required
def admin_delete_news(request, pk):
    news = get_object_or_404(TravelNews, pk=pk)

    if request.method == "POST":
        news.delete()
        return redirect('admin_news_list')

    return redirect('admin_news_list')



@staff_member_required
def admin_blog_list(request):
    blogs = Blog.objects.all().order_by('-date')
    return render(request, 'admin_blog_list.html', {
        'blogs': blogs
    })

@staff_member_required
def admin_add_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_blog_list')
    else:
        form = BlogForm()

    return render(request, 'admin_blog_form.html', {
        'form': form,
        'title': 'Add New Blog'
    })


# UPDATE BLOG
@staff_member_required
def admin_update_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('admin_blog_list')
    else:
        form = BlogForm(instance=blog)

    return render(request, 'admin_blog_form.html', {
        'form': form,
        'title': 'Update Blog'
    })


# DELETE BLOG
@staff_member_required
def admin_delete_blog(request, pk):
    blog = get_object_or_404(Blog, pk=pk)

    if request.method == "POST":
        blog.delete()
        return redirect('admin_blog_list')

    return redirect('admin_blog_list')



@staff_member_required
def admin_messages_list(request):
    messages = ContactMessage.objects.all().order_by("-created_at")
    return render(request, "messages_list.html", {"messages": messages})

@staff_member_required
def admin_message_detail(request, message_id):
    msg = get_object_or_404(ContactMessage, id=message_id)
    return render(request, "mesage_detail.html", {"msg": msg})

@staff_member_required
def admin_send_response(request, message_id):
    contact_msg = get_object_or_404(ContactMessage, id=message_id)

    user = User.objects.filter(email=contact_msg.email).first()

    if request.method == "POST":
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        if user:
            InboxMessage.objects.create(
                user=user,
                subject=subject,
                message=message
            )

        return redirect("admin_messages_list")

    return render(request, "compose_message.html", {
        "contact_msg": contact_msg,
        "user": user
    })


@staff_member_required
def admin_feedbacks_view(request):
    feedbacks = Feedback.objects.select_related('user', 'package').order_by('-created_at')
    return render(request, 'admin_feedback.html', {
        'feedbacks': feedbacks
    })


@staff_member_required
def admin_users_view(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_users.html', {'users': users})


# LIST COUNTRIES
@staff_member_required
def admin_country_list(request):
    countries = Country.objects.all()
    return render(request, 'admin_country_list.html', {
        'countries': countries
    })


# ADD COUNTRY
@staff_member_required
def admin_add_country(request):
    if request.method == 'POST':
        form = CountryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_country_list')
    else:
        form = CountryForm()

    return render(request, 'country_form.html', {
        'form': form,
        'title': 'Add Country'
    })


# EDIT COUNTRY
@staff_member_required
def admin_edit_country(request, pk):
    country = get_object_or_404(Country, pk=pk)

    if request.method == 'POST':
        form = CountryForm(request.POST, request.FILES, instance=country)
        if form.is_valid():
            form.save()
            return redirect('admin_country_list')
    else:
        form = CountryForm(instance=country)

    return render(request, 'country_form.html', {
        'form': form,
        'title': 'Edit Country'
    })


# DELETE COUNTRY
@staff_member_required
def admin_delete_country(request, pk):
    country = get_object_or_404(Country, pk=pk)
    country.delete()
    return redirect('admin_country_list')

@staff_member_required
def admin_booking_list(request):
    
    bookings = Booking.objects.order_by('-datetime')

    return render(request, 'admin_booking_list.html', {
        'bookings': bookings
    })



@staff_member_required
def admin_dashboard(request):
    total_packages = TravelPackage.objects.count()
    total_bookings = Booking.objects.count()  # total bookings
    total_users = User.objects.count()        # total registered users
    total_revenue = Booking.objects.aggregate(total=Sum('total_price'))['total'] or 0  # sum of all bookings

    context = {
        'total_packages': total_packages,
        'total_bookings': total_bookings,
        'total_users': total_users,
        'total_revenue': total_revenue,
    }

    return render(request, 'dashboard.html', context)

# ADMIN – LIST ALL PACKAGES
@staff_member_required
def admin_package_list(request):
    packages = TravelPackage.objects.all().order_by('-id')
    return render(request, 'admin_package_list.html', {
        'packages': packages
    })

# ADMIN – ADD NEW PACKAGE
@staff_member_required
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
@staff_member_required
def admin_delete_package(request, pk):
    package = get_object_or_404(TravelPackage, pk=pk)

    if request.method == 'POST':
        package.delete()
        return redirect('admin_package_list')

    return render(request, 'package_confirm_delete.html', {
        'package': package
    })

@staff_member_required
def admin_booking_update(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    if request.method == "POST":
        form = AdminBookingUpdateForm(request.POST, instance=booking)
        if form.is_valid():
            updated_booking = form.save(commit=False)

            # Optional: auto set cancelled_at
            if updated_booking.booking_status == "Cancelled":
                from django.utils import timezone
                updated_booking.cancelled_at = timezone.now()

            updated_booking.save()
            return redirect("admin_booking_list")  # your listing view name

    else:
        form = AdminBookingUpdateForm(instance=booking)

    return render(request, "admin_booking_update.html", {
        "form": form,
        "booking": booking
    })


