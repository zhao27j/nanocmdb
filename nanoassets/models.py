import uuid  # required for unique id
from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.


class ScrapRequest(models.Model):
    case_id = models.UUIDField(_("Request case ID"), primary_key=True,
                               default=uuid.uuid4, help_text='Unique ID for the particular request')
    REQUEST_STATUS = (
        ('I', 'Initialized'),
        ('A', 'Approved'),
    )
    status = models.CharField(
        _("Request status"), choices=REQUEST_STATUS, default='I', max_length=1)
    # instance = models.ForeignKey("nanoassets.Instance", verbose_name=_("Instance"), on_delete=models.SET_NULL, null=True, blank=True)
    requested_by = models.ForeignKey(User, verbose_name=_(
        "Requested by"), related_name='+', on_delete=models.SET_NULL, null=True, blank=True)
    requested_on = models.DateField(
        _("Requested on"), auto_now=False, auto_now_add=True, blank=True, null=True)
    approved_by = models.ForeignKey(User, verbose_name=_(
        "Approved by"), related_name='+', on_delete=models.SET_NULL, null=True, blank=True)
    approved_on = models.DateField(
        _("Approved on"), auto_now=False, auto_now_add=False, blank=True, null=True)

    def __str__(self):
        # return '%s Scrapping Request %s by %s on %s, Approved by %s on %s' % (self.case_id, self.status, self.requested_by, str(self.requested_on), self.approved_by, str(self.approved_on))
        return str(self.case_id)

    def get_absolute_url(self):
        return reverse("scrap-request-detail", kwargs={"pk": self.pk})
    
    class Meta:
        ordering = ['requested_on',]


class Instance(models.Model):
    serial_number = models.CharField(
        primary_key=True, max_length=20, help_text='enter serial #')
    model_type = models.ForeignKey("nanoassets.ModelType", verbose_name=_(
        "Model / Type"), on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(User, verbose_name=_(
        "Owner"), on_delete=models.SET_NULL, null=True, blank=True)
    INSTANCE_STATUS = (
        ('A', 'Available'),
        ('U', 'in Use'),
        ('R', 'in Repair'),
        ('S', 'Scrapped')
    )
    status = models.CharField(max_length=15, choices=INSTANCE_STATUS,
                              default='Available', help_text='Asset availability')

    eol_date = models.DateField(null=True, blank=True)
    scrap_request = models.ForeignKey("nanoassets.ScrapRequest", verbose_name=_(
        "Scrap Request"), on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overeol(self):
        if self.eol_date and date.today() > self.eol_date:
            return True
        return False

    def __str__(self):
        # return '%s (%s, %s, %s)' % (self.serial_number, self.model_type.manufacturer, self.model_type.name, self.owner)
        return self.serial_number

    def get_absolute_url(self):
        return reverse("instance-detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ['model_type', 'eol_date',]


class ModelType(models.Model):
    name = models.CharField(max_length=20)
    manufacturer = models.ForeignKey(
        "Manufacturer", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.manufacturer, self.name)

    def get_absolute_url(self):
        return reverse("modeltype-detail", kwargs={"pk": self.pk})


class Manufacturer(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name
