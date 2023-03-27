from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Manufacturer(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
class Instance(models.Model):
    serial_number = models.CharField(primary_key=True, max_length=20, help_text='enter serial #')
    model_type = models.ForeignKey("nanoassets.ModelType", verbose_name=_("Model / Type"), on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(User, verbose_name=_("Owner"), on_delete=models.SET_NULL, null=True, blank=True)

    INSTANCE_STATUS = (
        ('Maintenance', 'in Repair'),
        ('Available', 'spare'),
        ('In use', 'in Use'),
    )

    status = models.CharField(max_length=15, choices=INSTANCE_STATUS, default='Available', help_text='Asset availability')
    eol_date = models.DateField(null=True, blank=True)

    @property
    def is_overeol(self):
        if self.eol_date and date.today() > self.eol_date:
            return True
        return False

    def __str__(self):
        return '%s (%s, %s, %s)' % (self.serial_number, self.model_type.manufacturer, self.model_type.name, self.owner)
    
    def get_absolute_url(self):
        return reverse("instance-detail", kwargs={"pk": self.pk})
    
    class Meta:
        ordering = ['model_type']
    
class ModelType(models.Model):
    name = models.CharField(max_length=20)
    manufacturer = models.ForeignKey("Manufacturer", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.manufacturer, self.name)
    
    def get_absolute_url(self):
        return reverse("modeltype-detail", kwargs={"pk": self.pk})
    