from django import forms

from django.contrib.auth.models import User

from .models import UserProfile

class UpadteUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control',}))
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form-control',}))
    
    class Meta:
        model = User
        fields = ['username', 'email',]


class UpdateUserProfileForm(forms.ModelForm):
    # avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file',}))
    cellphone = forms.NumberInput(widget=forms.NumberInput(attrs={
        'class': 'form-control',
    }))

    class Meta:
        model = UserProfile
        fields = ['cellphone',]