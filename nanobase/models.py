from django.db import models

from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, verbose_name=_("User Profile"), on_delete=models.CASCADE)
    # avatar = models.ImageField(_(""), upload_to=None, height_field=None, width_field=None, max_length=None)
    # dept = 
    cellphone = models.DecimalField(_("Cellphone"), max_digits=11, decimal_places=0, null=True, blank=True)

    def __str__(self):
        return self.user.username
    