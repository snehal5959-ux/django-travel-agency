from django.urls import path
from . import views


#payment success

urlpatterns = [
#account_settings inbox profile
    # Home
    path('', views.travel_package_list, name='home'),
    path('profile/', views.profile, name='profile'), 

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout_view'),

    # Packages
    path('packages/', views.travel_package_list, name='travel_package_list'),

    # Booking
    path('book/<int:pk>/', views.book_package, name='book_package'),
    path('booking/<int:package_id>/', views.booking_handler_view, name='booking_handler_view'),

    # Booking Result
    path("submit-booking/<int:package_id>/", views.submit_booking, name="submit_booking"),
    
    path('fail/', views.booking_fail, name='booking_fail'),
    path(
    "packages/<int:package_id>/submit-booking/",views.submit_booking,name="submit_booking"
),
path("booking-success/", views.booking_success, name="booking_success"),

 path('reset-password/', views.reset_password, name='reset_password'),

    # Recommendations
    path('recommendations/', views.packages_recommendations, name='packages_recommendations'),

    # Payment
    path("create-order/", views.create_order, name="create_order"),
    path("payment/<int:booking_id>/", views.payment_page, name="payment_page"),
    path("payment-success/", views.payment_success, name= "payment_success"),
path("payment-success/<int:booking_id>/", views.payment_success, name="payment_success"),

    # Static Pages ai_chatbot
    path('contact/', views.contact, name='contact'),
    path('blog/', views.blog, name='blog'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('feedback/', views.feedback_view, name='feedback'),
    path('my-bookings/', views.booking_history_view, name='booking_history_view'),
   
    path('booking/<int:booking_id>/cancel/', views.cancel_booking_view, name='cancel_booking'),
    path('add-to-favourites/<int:id>/', views.add_to_favourites, name='add_to_favourites'),
    
     path('search/', views.search_packages, name='search_packages'),

    
    path('', views.travel_package_list, name='travel_package_list'),
    path('booking/<int:package_id>/', views.booking_handler_view, name='booking_handler_view'),
    path('favourites/', views.add_to_favourites, name='add_to_favourites'),
        path('packages/favourite/<int:package_id>/', views.add_to_favourites, name='add_to_favourites'),
    path('packages/favourites/', views.favourites_list, name='favourites_list'),
    path('packages/<int:package_id>/', views.travel_package_detail, name='travel_package_detail'),
path('allnews/', views.travel_news_list, name="travel_news_list"),
path('countries/', views.countries, name='countries'),
path('countries/<str:country_name>/places/', views.country_places, name='country_places'),

 path('account/settings/', views.account_settings, name='account_settings'),
    path('history/', views.booking_history_view, name='booking_history'),
path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
path('booking/<int:booking_id>/refund/', views.refund_booking, name='refund_booking'),
path("payment-success/", views.payment_success, name="payment_success"),
path("create-razorpay-order/", views.create_razorpay_order, name="create_razorpay_order"),
path("inbox/", views.user_inbox, name="user_inbox"),
path("payment-success/", views.payment_success, name="payment_success"),
path("request-refund/<int:pk>/", views.request_refund, name="request_refund"),
    path(
        'debug-booking/<int:package_id>/',
        views.debug_booking,
        name='debug_booking'
    ),
      path(
        "inbox/<int:message_id>/",
        views.inbox_message_detail,
        name="inbox_message_detail"
    ),
 path("invoice/<int:booking_id>/", views.invoice_view, name="invoice_view"),
 path(
    "invoice/<int:booking_id>/pdf/",
    views.invoice_pdf,
    name="invoice_pdf"
),

path("compose/", views.compose_message, name="compose_message"),

] 












