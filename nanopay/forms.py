# from django.core.exceptions import ValidationError
# from django.utils.translation import gettext_lazy as _

# from django import forms
from django.forms import ModelForm, modelformset_factory
# from django.conf import settings
# from django.core.mail import send_mail

from .models import PaymentTerm


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