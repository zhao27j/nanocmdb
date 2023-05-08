# from django.conf import settings
# from django.core.mail import send_mail

import datetime

from django import forms
from django.forms import ModelForm, modelformset_factory

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import PaymentTerm


class NewContractForm(forms.Form):
    briefing = forms.CharField(required=True, help_text=(_('briefing')))
    
    # party_a_list = forms.MultipleChoiceField()
    # party_b_list = forms.MultipleChoiceField()

    CONTRACT_TYPE = (
        ('M', 'Maintenance'),
        ('N', 'New'),
        ('R', 'Rental'),
        ('E', 'Expired'),
    )
    # type = forms.ChoiceField(initial='M', choices=[CONTRACT_TYPE], required=True, help_text=(_('Type')))
    startup = forms.DateField(initial=datetime.date.today, required=True, help_text=(_('Start time')))
    endup = forms.DateField(initial=datetime.date.today, required=True, help_text=(_('End time')))
    # scanned_copy = forms.FileField(required=True, help_text=(_('Scanned copy')))


    def clean_startup(self):
        data = self.cleaned_data["startup"]
        
        return data
    
    def clean_contract_duration(self):
        data = self.cleaned_data["startup", "endup"]

        # Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_("invalid date - renewal in past"))

        # Check date is in range librarian allowed to change (+4 weeks).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_("Invalid date - renewal more than 4 weeks ahead"))

        # Remember to always return the cleaned data.
        return data


PaymentTermFormSet = modelformset_factory(
    PaymentTerm,
    fields=[
        "pay_day", "plan", "amount",
    ],
    extra=1
)

class PaymentTermFrom(ModelForm):
    class Meta:
        model = PaymentTerm
        fields = ["pay_day", "plan", "amount", ]


"""
class RenewBookmodelForm(forms.ModelForm):
    class Meta:
        model = BookInstance
        fields = ["due_back"]
        labels = {
            "due_back": _("Renewal date"),
        }
        help_texts = {
            "due_back": _("Enter a date between now and 4 weeks (default 3)."),
        }

    def clean_due_back(self):
        data = self.cleaned_data["due_back"]

        # check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_("Invalid date - renewal in past"))

        # check date is in range librarian allowed to change (+4 weeks)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_("Invalid date - renewal more than 4 weeks ahead"))

        return data
"""