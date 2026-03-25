from django.http import HttpResponse
from django.shortcuts import render
from django.db.utils import OperationalError
from django.db.models import Prefetch

from news.models import TravelNews
from packages.models import TravelPackage, Country
from news.views import update_image_url
from .models import Gallery


def index(request):
    """
    Homepage view (SAFE for Railway deployment)
    """

    # ✅ SAFE: Travel News (prevents crash if table not created yet)
    try:
        page_obj = list(TravelNews.objects.all().order_by('-id')[:3])
        for article in page_obj:
            article.image_url = update_image_url(
                article.image_url,
                {'w': 500, 'h': '400', 'fit': 'crop', 'q': 75}
            )
    except OperationalError:
        page_obj = []

    # ✅ SAFE: Travel Packages
    try:
        travel_packages = TravelPackage.objects.prefetch_related('tags').filter(available=True)[:6]
    except OperationalError:
        travel_packages = []

    # ✅ SAFE: Countries
    try:
        countries = Country.objects.all()[:12]
    except OperationalError:
        countries = []

    ratings_range = range(1, 6)

    return render(request, 'index.html', {
        'page_obj': page_obj,
        'packages': travel_packages,
        'ratings_range': ratings_range,
        'countries': countries
    })


def not_found(request, exception=None):
    """
    Custom 404 page
    """
    return render(request, '404.html', status=404)


def gallery_view(request):
    """
    Gallery page (SAFE)
    """
    try:
        images = Gallery.objects.all().order_by('-created_at')
    except OperationalError:
        images = []

    return render(request, 'gallery.html', {
        'images': images
    })