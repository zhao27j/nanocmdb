from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from django.db import models

from nanoassets.models import Instance

# Create your models here.

def path_of_scanned_contract_copy(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    # fs = FileSystemStorage(location="/media/scanned_contract_copy/")
    return "scanned_contract_copy/user_{0}/{1}".format(instance.user.id, filename)
    

class Contract(models.Model):
    name = models.CharField(_("Contract Name"), max_length=50)
    party_a_list = models.ManyToManyField("nanopay.LegalEntity", verbose_name=_("甲方"), related_name='partyas')
    party_b_list = models.ManyToManyField("nanopay.LegalEntity", verbose_name=_("乙方"), related_name='partybs')
    party_c_list = models.ManyToManyField("nanopay.LegalEntity", verbose_name=_("丙方"), related_name='partycs', blank=True)
    startup = models.DateField(_("Start Up"))
    endup = models.DateField(_("End Up"))
    scanned_copy = models.FileField(_("Scanned Copy"), upload_to='scanned_contract_copy/', max_length=100, null=True, blank=True)
    assets = models.ManyToManyField(Instance, verbose_name=_("Related Assets"), blank=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('nanopay:contract-detail', kwargs={'pk': self.pk})
    
    def get_contract_duration_in_month(self):
        return self.endup - self.startup
    


class PaymentTerm(models.Model):
    pay_day = models.DateField(_("Pay Date"))
    amount = models.FloatField(_("Payment Amount"))
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


class Prjct(models.Model):
    name = models.CharField(_("Project Name"), max_length=20)

    def __str__(self):
        return self.name
