from django import forms
from .models import TravelPackage, Tag

class TravelPackageForm(forms.ModelForm):
    class Meta:
        model = TravelPackage
        fields = [
            'name', 'destination', 'package_type', 'price',
            'duration', 'rating', 'description', 'available',
            'tags', 'image'
        ]
        widgets = {
            'image': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter image URL here'
            })
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
   
