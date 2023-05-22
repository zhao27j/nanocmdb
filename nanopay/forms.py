# from django.conf import settings
# from django.core.mail import send_mail

import pathlib
# import datetime
from typing import Any, Dict

from django import forms
from django.forms import TextInput, Select, NumberInput, ClearableFileInput, modelformset_factory

from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404

from .models import Contract, LegalEntity, PaymentTerm, PaymentRequest

class NewPaymentRequestForm(forms.Form):
    non_payroll_expense = forms.CharField(required=True, max_length=128, widget=TextInput(attrs={
        "list": "non_payroll_expenses",
        "class": "form-control",
    }))

    amount = forms.DecimalField(required=True, max_digits=8, decimal_places=2, widget=NumberInput(attrs={
        "class": "form-control",
        "placeholder": "the amount presented on the invoice"
        }))
    scanned_copy = forms.FileField(required=True, help_text=".pdf is acceptable Only", 
                                   widget=ClearableFileInput(attrs={"class": "form-control",}))

    def clean(self):
        cleaned_data = super().clean()

        amount = cleaned_data.get('amount')
        if amount <= 0:
            raise ValidationError(_("amount must be a positive number"))

        scanned_copy = cleaned_data.get('scanned_copy')
        # scanned_copy_ext = pathlib.Path(scanned_copy.name).suffix
        if not pathlib.Path(scanned_copy.name).suffix in ['.pdf', ]:
            raise ValidationError(_("the Only acceptable format is .pdf for Scanned Copy"))
        
        if not scanned_copy.content_type == 'application/pdf':
            raise ValidationError(_("the Only acceptable format is .pdf for Scanned Copy"))

        # return super().clean()

        

class NewPaymentTermForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        
        contract = cleaned_data.get('contract')
        
        pay_day = cleaned_data.get('pay_day')
        if pay_day < contract.startup:
            raise ValidationError(_("the scheduled Pay date should NOT be later than the Start date defined in the Contract"))
        
        recurring = abs(cleaned_data.get('recurring'))
        if recurring == 0:
            raise ValidationError(_("the value of Recurring must be > 0"))

        plan = cleaned_data.get('plan')
        if plan == 'C' and recurring != 1:
            raise ValidationError(_("the Recurring for Custom plan must be = 1 "))
        
        amount = cleaned_data.get('amount')
        if amount <= 0:
            raise ValidationError(_("amount must be a positive number"))
        
        # return super().clean()
    
    class Meta:
        model = PaymentTerm
        fields = ["pay_day", "plan", "recurring", "amount", "contract"]
        widgets = {
            "pay_day": TextInput(attrs={"type": "date", "class": "form-control",}),
            "plan": Select(attrs={"class": "form-control",}),
            "recurring": NumberInput(attrs={"class": "form-control",}),
            "amount": NumberInput(attrs={"class": "form-control",}),
            "contract": Select(attrs={
                "disabled":True, 
                "class": "form-control", }),
        }
        labels = {
            "pay_day": _("Date"),
            "plan": _("Plan"),
            "recurring": _("Recurring"),
            "amount": _("Amount"),
            "coutract": _("Contract"),
        }
        help_texts = {
            "pay_day": _("payment date defined in the contract"),
            "plan": _("payment schedule defined in the contract"),
            "recurring": _("payment recurring defined in the contract"),
            "amount": _("payment acount defined in the contract"),
        }
        
        error_messages = {
            NON_FIELD_ERRORS: {
                "unique_together": "%(model_name)s's %(field_labels)s are not unique.",
            }
        }


class NewContractForm(forms.Form):
    briefing = forms.CharField(required=True, widget=forms.TextInput(attrs={"placeholder": "briefing the main purpose of the contract ...", "class": "form-control",}))
    
    party_a_list = forms.ModelMultipleChoiceField(required=True, queryset=None, widget=forms.SelectMultiple(attrs={"class": "form-select",}))
    party_b_list = forms.ModelMultipleChoiceField(required=True, queryset=None, widget=forms.SelectMultiple(attrs={"class": "form-select",}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["party_a_list"].queryset = LegalEntity.objects.filter(type='I')
        self.fields["party_b_list"].queryset = LegalEntity.objects.filter(type='E')
    
    non_payroll_expense = forms.CharField(required=True, max_length=100, widget=TextInput(attrs={
        "list": "non_payroll_expenses",
        "class": "form-control",
    }))

    CONTRACT_TYPE = (
        ('M', 'Maintenance'),
        ('N', 'New'),
        ('R', 'Rental'),
        # ('E', 'Expired'),
    )
    type = forms.ChoiceField(required=True, initial='M', choices=CONTRACT_TYPE, widget=forms.Select(attrs={"class": "form-control",}))

    startup = forms.DateField(widget=forms.TextInput(attrs={"type": "date", "class": "form-control",}), required=True, )
    endup = forms.DateField(widget=forms.TextInput(attrs={"type": "date", "class": "form-control",}), required=False)
    
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
        
        briefing = cleaned_data.get('briefing')
        contracts = Contract.objects.filter(briefing=briefing.strip())
        if contracts:
            raise ValidationError(_("contract with the same Briefing already exists"))

        startup = cleaned_data.get("startup")
        endup = cleaned_data.get("endup")
        if endup and endup < startup:
            raise ValidationError(_("the End date should NOT be later than the Start date"))

        scanned_copy = cleaned_data.get("scanned_copy")
        # scanned_copy_ext = pathlib.Path(scanned_copy.name).suffix
        if not pathlib.Path(scanned_copy.name).suffix in ['.pdf', ]:
            raise ValidationError(_("the Only acceptable format is .pdf for Scanned Copy"))
        
        if not scanned_copy.content_type == 'application/pdf':
            raise ValidationError(_("the Only acceptable format is .pdf for Scanned Copy"))

        # return super().clean()


"""

class PaymentTermFrom(ModelForm):
    class Meta:
        model = PaymentTerm
        fields = ["pay_day", "plan", "amount", ]


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


PaymentTermFormSet = modelformset_factory(
    PaymentTerm,
    fields=[
        "pay_day", "plan", "amount",
    ],
    extra=1
)
        
"""