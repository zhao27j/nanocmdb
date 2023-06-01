from django import forms

from django.contrib.auth.models import User

from .models import UserProfile


class UserProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = UserProfile

        fields = [
            # 'avatar',
            'cellphone',
            ]
        
        widgets = {
            # "avatar": forms.ImageField(attrs={'class': 'form-control-file',}),
            "cellphone": forms.NumberInput(attrs={'class': 'form-control',})
        }
