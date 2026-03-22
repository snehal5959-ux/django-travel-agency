from django.urls import path
from . import views

urlpatterns = [
   path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/packages/', views.admin_package_list, name='admin_package_list'),
    path('add/', views.admin_add_package, name='admin_add_package'),
    path('delete/<int:pk>/', views.admin_delete_package, name='admin_delete_package'),
    path('admin/bookings/', views.admin_booking_list, name='admin_booking_list'),
    path('admin/countries/', views.admin_country_list, name='admin_country_list'),
path('admin/countries/add/', views.admin_add_country, name='admin_add_country'),
path('admin/countries/edit/<int:pk>/', views.admin_edit_country, name='admin_edit_country'),
path('admin/countries/delete/<int:pk>/', views.admin_delete_country, name='admin_delete_country'),
path('admin/users/', views.admin_users_view, name='admin_users'),
path('admin/feedbacks/', views.admin_feedbacks_view, name='admin_feedbacks'),
 path("admin/messages/", views.admin_messages_list, name="admin_messages_list"),
    path("admin/messages/<int:message_id>/", views.admin_message_detail, name="admin_message_detail"),
    path("admin/messages/<int:message_id>/reply/", views.admin_send_response, name="admin_send_response"),
    path('admin/refund-requests/', views.admin_refund_requests, name='admin_refund_requests'),
    path("admin/bookings/update/<int:booking_id>/", views.admin_booking_update, name="admin_booking_update"),
    path('admin/blogs/', views.admin_blog_list, name='admin_blog_list'),
    path('admin/blogs/', views.admin_blog_list, name='admin_blog_list'),
path('admin/blogs/add/', views.admin_add_blog, name='admin_add_blog'),
path('admin/blogs/update/<int:pk>/', views.admin_update_blog, name='admin_update_blog'),
path('admin/blogs/delete/<int:pk>/', views.admin_delete_blog, name='admin_delete_blog'),
path('admin/news/', views.admin_news_list, name='admin_news_list'),
path('admin/news/add/', views.admin_add_news, name='admin_add_news'),
path('admin/news/update/<int:pk>/', views.admin_update_news, name='admin_update_news'),
path('admin/news/delete/<int:pk>/', views.admin_delete_news, name='admin_delete_news'),
    path("admin-gallery/", views.admin_gallery, name="admin_gallery"),
    path("delete-gallery/<int:id>/", views.delete_gallery, name="delete_gallery"),
    path('packages/update/<int:pk>/', views.admin_update_package, name='admin_update_package'),

]
