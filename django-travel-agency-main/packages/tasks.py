# Django Imports
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
from django.template.loader import render_to_string
from django.contrib.auth.models import User

# Local Imports
from .models import Booking, TravelPackage
from celery import shared_task


@shared_task
def send_confirmation_email(name, email, package_name, total_price):
    """
    Sends booking confirmation email
    """
    subject = f"Booking Confirmation for {package_name}"

    message = render_to_string('confirmation_email.html', {
        'name': name,
        'package_name': package_name,
        'total_price': total_price
    })

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        html_message=message
    )


# -----------------------------------
# SIMPLE RECOMMENDATION SYSTEM (NO AI LIBS)
# -----------------------------------
@shared_task
def package_recommendations(user_id):
    """
    Rule-based travel package recommendation system
    (Final Year Friendly – No NumPy / No ML)
    """

    user = User.objects.get(id=user_id)
    last_booking = Booking.objects.filter(email=user.email).last()

    # If no booking, show top-rated packages
    if not last_booking:
        return list(
            TravelPackage.objects.all()
            .order_by('-rating')
            .values_list('id', flat=True)[:3]
        )

    gender = last_booking.gender
    destination = last_booking.package.destination
    package_type = last_booking.package.package_type

    filters = Q()

    if gender == 'Male':
        filters &= Q(package_type__in=['Adventure', 'Beach', 'Cultural'])
    elif gender == 'Female':
        filters &= Q(package_type__in=['Family', 'Relaxation', 'Cultural'])

    filters &= Q(destination=destination) | Q(package_type=package_type)

    recommended_packages = (
        TravelPackage.objects
        .filter(filters)
        .order_by('-rating')[:3]
    )

    return [pkg.id for pkg in recommended_packages]
