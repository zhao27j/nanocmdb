from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django import forms
from django.conf import settings
from django.core.mail import send_mail

from .models import branchSite

class TransferBranchSite(forms.Form):    
    new_branchsite = forms.ChoiceField(
        label='Transfer to ...',
        # choices=[site_list],
        help_text="Enter a date between now and 4 weeks (default 3).",
        required=True)
    
    def clean_field(self):
        data = self.cleaned_data["new_branchsite"]
        
        if data == None:
            raise ValidationError(_('no Site name'))
        
        return data
    

class ContactForm(forms.Form):

    name = forms.CharField(max_length=20)
    email = forms.EmailField()
    inquiry = forms.CharField(max_length=70)
    message = forms.CharField(widget=forms.Textarea)

    def get_info(self):
        """ Method that returns formatted information: return: subject, msg """

        # Cleaned data
        cl_data = super.clean()

        name = cl_data.get('name').strip()
        from_email = cl_data('email')
        subject = cl_data('inquiry')

        msg = f'{name} with email {from_email} said:'
        msg += f'\n"{subject}"\n\n'
        msg += cl_data.get('message')

        return subject, msg
    
    def send(self):
        subject, msg = self.get_info()

        send_mail(
            subject=subject,
            message=msg,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.RECIPIENT_ADDRESS],
        )


