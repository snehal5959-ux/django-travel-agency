from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import TravelPackage, Booking
from .forms import TravelPackageForm

# ❌ Removed generate_pdf_invoice
from .tasks import send_confirmation_email, package_recommendations
from .utils import validate_booking, calculate_total_price, generate_flouci_payment

from decimal import Decimal
from datetime import datetime


def book_package(request, pk):
    package = get_object_or_404(TravelPackage, pk=pk)
    return render(request, 'travel_package_booking.html', {'package': package})


def travel_package_list(request):
    travel_packages = TravelPackage.objects.all()
    ratings_range = range(1, 6)
    return render(
        request,
        'travel_package_list.html',
        {'packages': travel_packages, 'ratings_range': ratings_range}
    )


def booking_handler_view(request, package_id):
    package = get_object_or_404(TravelPackage, id=package_id)
    child_discount = Decimal('0.5')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        booking_date = request.POST.get('datetime')
        num_adults = int(request.POST.get('SelectPerson', 0))
        num_children = int(request.POST.get('SelectKids', 0))
        gender = request.POST.get('SelectGender', 'None')
        payment_method = request.POST.get('payment_method', '0')
        consent = request.POST.get('consent')

        errors = validate_booking(
            name, email, booking_date,
            num_adults, num_children,
            payment_method, consent
        )

        if errors:
            return render(request, 'travel_package_booking.html', {
                'package': package,
                'name': name,
                'email': email,
                'booking_date': booking_date,
                'num_adults': num_adults,
                'num_children': num_children,
                'gender': gender,
                'payment_method': payment_method,
                'errors': errors
            })

        total_price = calculate_total_price(
            package, num_adults, num_children, child_discount
        )

        booking = Booking.objects.create(
            package=package,
            name=name,
            email=email,
            datetime=datetime.strptime(booking_date, '%Y-%m-%d'),
            num_adults=num_adults,
            num_children=num_children,
            total_price=total_price,
            gender=gender,
            payment_status='Pending',
            payment_method=payment_method
        )

        # ONLINE PAYMENT
        if payment_method == "Online":
            payment_url = generate_flouci_payment(total_price)

            if payment_url:
                booking.payment_status = 'Paid'
                booking.save()

                send_confirmation_email.apply_async(
                    args=[name, email, package.name, total_price]
                )

                return HttpResponseRedirect(payment_url)

            booking.delete()
            return redirect(reverse('booking_fail'))

        # OFFLINE PAYMENT
        send_confirmation_email.apply_async(
            args=[name, email, package.name, total_price]
        )

        return redirect(reverse('booking_success'))

    return render(request, 'travel_package_booking.html', {'package': package})


def packages_recommendations(request):
    result = package_recommendations.apply_async(args=[request.user.id])
    recommended_package_ids = result.get()

    top_recommendations = TravelPackage.objects.filter(
        id__in=recommended_package_ids
    )

    return render(
        request,
        'recommendations.html',
        {'packages': top_recommendations}
    )


def booking_success(request):
    return render(request, 'booking_success.html')


def booking_fail(request):
    return render(request, 'booking_fail.html')
