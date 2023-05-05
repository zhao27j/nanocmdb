from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django import forms
from django.conf import settings
from django.core.mail import send_mail

from .models import Contract




