# from django.conf import settings
# from django.core.mail import send_mail

import pathlib
# import datetime
from typing import Any, Dict

from django import forms
from django.forms import ModelForm, modelformset_factory

from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.utils.translation import gettext_lazy as _

from .models import Contract, LegalEntity, PaymentTerm

class NewPaymentTermForm(forms.ModelForm):
    class Meta:
        model = PaymentTerm
        fields = "__all__"
        error_messages = {
            NON_FIELD_ERRORS: {
                "unique_together": "%(model_name)s's %(field_labels)s are not unique.",
            }
        }


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class NewContractForm(forms.Form):
    briefing = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "Briefing", "class": "form-control",}))
    
    party_a_list = forms.ModelMultipleChoiceField(required=True, queryset=None, widget=forms.SelectMultiple(attrs={"class": "form-select",}))
    party_b_list = forms.ModelMultipleChoiceField(required=True, queryset=None, widget=forms.SelectMultiple(attrs={"class": "form-select",}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["party_a_list"].queryset = LegalEntity.objects.filter(type='I')
        self.fields["party_b_list"].queryset = LegalEntity.objects.filter(type='E')
    
    CONTRACT_TYPE = (
        ('M', 'Maintenance'),
        ('N', 'New'),
        ('R', 'Rental'),
        # ('E', 'Expired'),
    )
    type = forms.ChoiceField(required=True, initial='M', choices=CONTRACT_TYPE, widget=forms.Select(attrs={"class": "form-control",}))

    startup = forms.DateField(required=True, widget=forms.TextInput(attrs={"type": "date", "class": "form-control",}))
    endup = forms.DateField(required=True, widget=forms.TextInput(attrs={"type": "date", "class": "form-control",}))
    
    # scanned_copy = MultipleFileField(required=True)
    scanned_copy = forms.FileField(required=True, widget=forms.ClearableFileInput(attrs={
        # "multiple": True,
        "class": "form-control",
        }))
    """
    def clean_scanned_copy(self):
        data = self.cleaned_data["scanned_copy"]
        if pathlib.Path(data.name).suffix != '.pdf':
            raise ValidationError(_('the Only acceptable format is .pdf for Scanned Copy'))
        else:
            pass
        return data
    """

    def clean(self):
        cleaned_data = super().clean()

        startup = cleaned_data.get("startup")
        endup = cleaned_data.get("endup")
        if endup < startup:
            raise ValidationError(_("the End date should NOT be later than the Start date"))

        scanned_copy = cleaned_data.get("scanned_copy")
        # scanned_copy_ext = pathlib.Path(scanned_copy.name).suffix
        if not pathlib.Path(scanned_copy.name).suffix in ['.pdf', ]:
            raise ValidationError(_("the Only acceptable format is .pdf for Scanned Copy"))
        
        if not scanned_copy.content_type == 'application/pdf':
            raise ValidationError(_("the Only acceptable format is .pdf for Scanned Copy"))

        # return super().clean()

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