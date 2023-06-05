from django.utils.translation import gettext_lazy as _

from django import forms
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

from django.contrib.auth.models import User

from .models import UserProfile


class UserProfileUpdateForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()

        cellphone = cleaned_data.get('cellphone')
        if not cellphone or cellphone < 1 or len(str(cellphone)) < 11:
            raise ValidationError(_('invalid cellphone number'))

        # return super().clean()

    class Meta:
        model = UserProfile

        fields = [
            # 'avatar', 'dept', 'title', 
            'work_phone', 'postal_addr', 'cellphone',
            ]
        
        widgets = {
            # "avatar": forms.ImageField(attrs={'class': 'form-control-file',}),
            # "dept": forms.TextInput(attrs={'class': 'form-control',}),
            # "title": forms.TextInput(attrs={'class': 'form-control',}),
            "work_phone": forms.NumberInput(attrs={'class': 'form-control',}),
            "postal_addr": forms.TextInput(attrs={'class': 'form-control',}),
            "cellphone": forms.NumberInput(attrs={'class': 'form-control',}),
        }
