from django.http import HttpResponse
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import TravelNews
from .serializers import TravelNewsSerializer
from .tasks import scrape_travel_news  
from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from urllib.parse import urlparse, urlunparse, urlencode
from celery.result import AsyncResult

def index(request):
    return HttpResponse("Welcome to the News app!")

class TravelNewsListView(ListAPIView):
    queryset = TravelNews.objects.all().order_by('-published_date')
    serializer_class = TravelNewsSerializer

    # Add filtering, searching, and ordering functionality
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['published_date']  # Filter by published_date
    search_fields = ['title', 'content']  # Search by title or content
    ordering_fields = ['published_date', 'title']  # Allow ordering by date or title


def update_image_url(url, new_params):
    if not url:
        return url  # prevents None crash

    parsed_url = urlparse(str(url))
    safe_params = {k: str(v) for k, v in new_params.items()}
    new_query = urlencode(safe_params)
    updated_url = parsed_url._replace(query=new_query)
    return urlunparse(updated_url)

def display_travel_news(request):
    articles = TravelNews.objects.all().order_by('-published_date')

    paginator = Paginator(articles, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'travel_news_list.html', {
        'page_obj': page_obj
    })
