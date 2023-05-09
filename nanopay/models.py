from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django.db import models

from nanoassets.models import Instance

# Create your models here.

def path_of_contract_scanned_copy(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    # fs = FileSystemStorage(location="/media/scanned_contract_copy/")
    # return "scanned_contract_copy/user_{0}/{1}".format(instance.user.id, filename)
    # return "contract_scanned_copy/year_{0}/{1}".format(instance.startup.year, filename)
    pass

class Contract(models.Model):
    briefing = models.CharField(_("Briefing"), max_length=50, null=True)
    party_a_list = models.ManyToManyField("nanopay.LegalEntity", verbose_name=_("甲方"), related_name='partyas')
    party_b_list = models.ManyToManyField("nanopay.LegalEntity", verbose_name=_("乙方"), related_name='partybs')
    CONTRACT_TYPE = (
        ('M', 'Maintenance'),
        ('N', 'New'),
        ('R', 'Rental'),
        ('E', 'Expired'),
    )
    type = models.CharField(_("Contract Type"), choices=CONTRACT_TYPE, default='M', max_length=1)
    startup = models.DateField(_("Start Up"), null=True)
    endup = models.DateField(_("End Up"), null=True)
    scanned_copy = models.FileField(_("Scanned Copy"), upload_to='contract_scanned_copy/', max_length=100, null=True, blank=True)
    assets = models.ManyToManyField(Instance, verbose_name=_("Related Assets"), blank=True)

    def __str__(self):
        return str(self.briefing)
    
    def get_absolute_url(self):
        return reverse('nanopay:contract-detail', kwargs={'pk': self.pk})
    
    def get_contract_duration_in_month(self):
        # return (self.endup.year - self.startup.year) * 12 + (self.endup.month - self.startup.month)
        pass

    def get_prjct(self):
        for party in self.party_a_list.all():
            if  party.type == 'I':
                return party.prjct
        for party in self.party_b_list.all():
            if  party.type == 'I':
                return party.prjct
    
    def get_parties_display(self):
        """ Creates a string for the Onsite IT Support. This is required to display Onsite IT Support in Admin. """
        return ", ".join([party_a.name for party_a in self.party_a_list.all()]) + ", " + ", ".join([party_b.name for party_b in self.party_b_list.all()])
    
    class Meta:
        ordering = ['startup', ]


class PaymentTerm(models.Model):
    pay_day = models.DateField(_("Date"))
    PAYMENT_PLAN = (
        ('M', 'Monthly'),
        ('Q', 'Quarterly'),
        ('S', 'Semi-anually'),
        ('A', 'Anually'),
        ('C', 'Custom'),
    )
    plan = models.CharField(_("Plan"), choices=PAYMENT_PLAN, default='M', max_length=1)
    amount = models.FloatField(_("Amount"))
    # paid = models.BooleanField(_("Paid"), default=False)
    paid_on = models.DateField(_("Paid on"), null=True, blank=True)
    contract = models.ForeignKey("nanopay.Contract", verbose_name=_("Contract"), on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "%s, %s" % (self.pay_day, self.amount)
    


class LegalEntity(models.Model):
    name = models.CharField(_("Legal Entity Name"), max_length=50)
    ENTITY_TYPE = (
        ('I', 'Internal'),
        ('E', 'External'),
    )
    type = models.CharField(_("Legal Entity Type"), choices=ENTITY_TYPE, default='E', max_length=1)
    prjct = models.ForeignKey("nanopay.Prjct", verbose_name=_("Project Name"), on_delete=models.SET_NULL, null=True, blank=True)
    deposit_bank = models.CharField(_("开户行"), max_length=50, null=True)
    deposit_bank_account = models.CharField(_("开户行账号"), max_length=25, null=True)
    tax_number = models.CharField(_("纳税人识别号"), max_length=25, null=True, blank=True)
    reg_addr = models.CharField(_("注册/工作地址"), max_length=50, null=True)
    reg_phone = models.CharField(_("注册/工作电话"), max_length=15, null=True)

    def __str__(self):
        return "%s, %s (%s)" % (self.type, self.name, self.prjct)
    
    def get_absolute_url(self):
        return reverse('nanopay:legalentity-detail', kwargs={'pk': self.pk})
    
    class Meta:
        ordering = ['type', 'name', ]


class Prjct(models.Model):
    name = models.CharField(_("Project Name"), max_length=20)

    def __str__(self):
        return self.name
