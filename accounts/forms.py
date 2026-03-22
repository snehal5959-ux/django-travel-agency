from django import forms
from packages.models import TravelPackage
from packages.models import Country
from packages.models import Booking

from packages.models import Blog
from news.models import TravelNews

class TravelNewsForm(forms.ModelForm):
    class Meta:
        model = TravelNews
        fields = '__all__'

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'slug', 'image', 'short_desc', 'full_content']
        widgets = {
            'short_desc': forms.Textarea(attrs={'rows': 3}),
            'full_content': forms.Textarea(attrs={'rows': 6}),
        }

class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = [
            'name', 
            'cover_image',
            'place1_name', 'place1_image', 'place1_description',
            'place2_name', 'place2_image', 'place2_description',
            'place3_name', 'place3_image', 'place3_description',
            'place4_name', 'place4_image', 'place4_description',
        ]



class TravelPackageForm(forms.ModelForm):
    class Meta:
        model = TravelPackage
        fields = [
            'name',
            'destination',
            'package_type',
            'price',
            'duration',
            'rating',
            'description',
            'available',
            'image',
            'tags',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class AdminBookingUpdateForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'payment_status',
            'booking_status',
            'refund_status',
            'refund_requested',
            'cancel_reason',
            
        ]