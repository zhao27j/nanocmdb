from django.db import models

from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    category = models.CharField(_("Category"), max_length=32, unique=True)

class UserDept(models.Model):
    dept = models.CharField(_("Department"), max_length=64, unique=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name=_("User Profile"), on_delete=models.CASCADE)
    # avatar = models.ImageField(_(""), upload_to=None, height_field=None, width_field=None, max_length=None)
    dept = models.ForeignKey("nanobase.UserDept", verbose_name=_(""), on_delete=models.SET_NULL, null=True, blank=True)
    cellphone = models.DecimalField(_("Cellphone"), max_digits=11, decimal_places=0, null=True, blank=True)
    work_phone = models.DecimalField(_("Cellphone"), max_digits=8, decimal_places=0, null=True, blank=True)

    postal_addr = models.CharField(_("Postal Address"), max_length=64, null=True, blank=True)

    legal_entity = models.ForeignKey("nanopay.LegalEntity", verbose_name=_(""), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username
    