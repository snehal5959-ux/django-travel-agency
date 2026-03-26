from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

handler404 = 'home.views.not_found'

# Non-translated URLs
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]

# Language aware URLs
urlpatterns += i18n_patterns(
    path('', include('home.urls')),
    path('packages/', include('packages.urls')),
    path('news/', include('news.urls')),
    path('support/', include('support.urls')),
    path('accounts/', include('accounts.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    