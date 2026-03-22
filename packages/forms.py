from django import forms
from django.contrib.auth.models import User
from .models import UserProfile  

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False, label="First Name")
    last_name = forms.CharField(max_length=30, required=False, label="Last Name")
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    phone = forms.CharField(max_length=20, required=False, label="Phone")
    gender = forms.ChoiceField(choices=[('Male','Male'),('Female','Female'),('Other','Other')], required=False)
    company = forms.CharField(max_length=100, required=False, label="Company")

    class Meta:
        model = UserProfile
        fields = ['phone', 'gender', 'company']
