import uuid  # required for unique id
from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# from django.utils import timezone

from smart_selects.db_fields import ChainedForeignKey

from django.utils.translation import gettext_lazy as _


# Create your models here.

"""
class ActivityHistory(models.Model):
    description = models.TextField(_("Description"))
    # created_on = models.DateTimeField(_("Created on"), auto_now=False, auto_now_add=True)
    # created_by = models.ForeignKey(User, verbose_name=(_("Created by")), on_delete=models.SET_NULL, null=True)
    Instance = models.ForeignKey("nanoassets.Instance", verbose_name=(_("IT Assets")), on_delete=models.SET_NULL, null=True, blank=True)
    Contract = models.ForeignKey("nanopay.Contract", verbose_name=(_("Contract")), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.description
    
    class Meta:
        ordering = ['-description',]
"""

class branchSite(models.Model):
    name = models.CharField(_("Site / Branch Office Name"), max_length=64, null=True)
    # project = models.ForeignKey("nanoassets.Model", verbose_name=(_("Affiliated with a project")), on_delete=models.SET_NULL, blank=True, null=True)

    country = models.ForeignKey("cities_light.Country", verbose_name=(_("Country")), on_delete=models.SET_NULL, null=True)
    region = ChainedForeignKey("cities_light.Region", chained_field='country', chained_model_field='country', show_all=False, auto_choose=True, sort=True, null=True)
    city = ChainedForeignKey('cities_light.City', chained_field='region', chained_model_field='region', show_all=False, auto_choose=True, sort=True, null=True)
    addr = models.CharField(_("Site Address"), max_length=256, null=True)
    postal = models.PositiveIntegerField(_("Postal code"), null=True)

    onSiteTech = models.ManyToManyField(User, verbose_name=(_("Onsite IT Support")), limit_choices_to={
        # "is_staff": True
        'groups__name': 'IT China'
    },)

    def __str__(self):
        return self.name

    def display_onSiteTech(self):
        """ Creates a string for the Onsite IT Support. This is required to display Onsite IT Support in Admin. """
        return ", ".join([onSiteTech.get_full_name() for onSiteTech in self.onSiteTech.all()[:5]])


class ScrapRequest(models.Model):
    case_id = models.UUIDField(_("Request case ID"), primary_key=True, default=uuid.uuid4, help_text='Unique ID for the particular request')
    REQUEST_STATUS = (
        ('I', 'Initialized'),
        ('A', 'Approved'),
    )
    status = models.CharField(_("Request status"), choices=REQUEST_STATUS, default='I', max_length=1)
    # instance = models.ForeignKey("nanoassets.Instance", verbose_name=(_("Instance")), on_delete=models.SET_NULL, null=True, blank=True)
    requested_by = models.ForeignKey(User, verbose_name=(_("Requested by")), related_name='+', on_delete=models.SET_NULL, null=True, blank=True)
    requested_on = models.DateField(_("Requested on"), auto_now=False, auto_now_add=True, blank=True, null=True)
    approved_by = models.ForeignKey(User, verbose_name=(_("Approved by")), related_name='+', on_delete=models.SET_NULL, null=True, blank=True)
    approved_on = models.DateField(_("Approved on"), auto_now=False, auto_now_add=False, blank=True, null=True)

    def __str__(self):
        # return '%s Scrapping Request %s by %s on %s, Approved by %s on %s' % (self.case_id, self.status, self.requested_by, str(self.requested_on), self.approved_by, str(self.approved_on))
        return str(self.case_id)

    def get_absolute_url(self):
        # return reverse("nanoassets:scrap-request-detail", kwargs={"pk": self.pk})
        return reverse("nanoassets:instance-scrapping-request-detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ['requested_on',]


class Instance(models.Model):
    serial_number = models.CharField(_("Serial #"), primary_key=True, max_length=32, default=uuid.uuid4, help_text='enter serial #')
    model_type = models.ForeignKey("nanoassets.ModelType", verbose_name=(_("Model / Type")), on_delete=models.SET_NULL, null=True, blank=True)
    owner = models.ForeignKey(User, verbose_name=(_("Owner")), on_delete=models.SET_NULL, null=True, blank=True)
    INSTANCE_STATUS = (
        ('AVAILABLE', 'Available'),
        ('inUSE', 'in Use'),
        ('inREPAIR', 'in Repair'),
        ('SCRAPPED', 'Scrapped'),
        ('buyBACK', 'BuyBack'),
        ('reUSE', 'Reuse'),
    )
    status = models.CharField(_("Status"), max_length=16, choices=INSTANCE_STATUS,default='Available', help_text='Asset availability')

    hostname = models.CharField(_("Hostname"), max_length=64, null=True, blank=True)
    # configuragion = models.ForeignKey("nanoassets.Configuragion", verbose_name=(_("Configuragion")), on_delete=models.SET_NULL, null=True, blank=True)

    scrap_request = models.ForeignKey("nanoassets.ScrapRequest", verbose_name=(_("Scrap Request")), on_delete=models.SET_NULL, null=True, blank=True)

    eol_date = models.DateField(null=True, blank=True)

    @property
    def is_overeol(self):
        if self.eol_date and date.today() > self.eol_date:
            return True
        return False

    branchSite = models.ForeignKey("nanoassets.branchSite", verbose_name=(_("Site / Branch Office")), on_delete=models.SET_NULL, null=True)
    
    # activity_history = models.ForeignKey("nanoassets.ActivityHistory", verbose_name=(_("Activity History")), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        # return '%s (%s, %s, %s)' % (self.serial_number, self.model_type.manufacturer, self.model_type.name, self.owner)
        return self.serial_number

    def get_absolute_url(self):
        return reverse("nanoassets:instance-detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ['model_type__sub_category', 'branchSite', 'status', 'model_type', 'eol_date',]


class ModelType(models.Model):
    name = models.CharField(max_length=32, unique=True)
    manufacturer = models.ForeignKey("Manufacturer", verbose_name=(_("Manufacturer")), on_delete=models.SET_NULL, blank=True, null=True)
    sub_category = models.ForeignKey("nanobase.SubCategory", verbose_name=(_("Sub-Catetory")), on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.manufacturer, self.name)

    def get_absolute_url(self):
        return reverse("nanoassets:modeltype-detail", kwargs={"pk": self.pk})
    
    class Meta:
        ordering = ['sub_category', 'manufacturer', 'name', ]


class Manufacturer(models.Model):
    name = models.CharField(max_length=16)

    def __str__(self):
        return self.name
