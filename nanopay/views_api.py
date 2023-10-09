
from django.utils import timezone

from django.core.exceptions import FieldDoesNotExist

from django.http import JsonResponse

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import LegalEntity, Prjct
from nanobase.models import UserProfile, ChangeHistory


@login_required
def legal_entity_new(request):
    if request.method == 'POST':
        # legal_entity, created = LegalEntity.objects.get_or_create(name=request.POST.get('name'))
        chg_log = ''
        try:
            legal_entity = LegalEntity.objects.get(pk=request.POST.get('pk'))
            created = False
        except LegalEntity.DoesNotExist:
            legal_entity = LegalEntity.objects.create()
            created = True

        for k, v in request.POST.items():
            try:
                LegalEntity._meta.get_field(k)

                if created:
                    chg_log = '1 x new Legal Entity [ ' + legal_entity.name + ' ] was added'
                else:
                    chg_log += 'The ' + k.capitalize() + ' was changed from [ ' + getattr(legal_entity, k) + ' ] to [ ' + v + ' ]; '
                    setattr(legal_entity, k, v)

                if k == 'prjct':
                    legal_entity.prjct = Prjct.objects.get(name=v) if request.POST.get('type') == 'I' else None
                elif k == 'contact' and v != '':
                    contact = User.objects.get(username=request.POST.get('contact').split("-")[-1].split("@")[0].strip())
                    contact.userprofile.legal_entity = legal_entity
                    contact.userprofile.save()
                else:
                    setattr(legal_entity, k, v)

                """
                    legal_entity.name = request.POST.get('name')
                    legal_entity.type = request.POST.get('type')
                    legal_entity.prjct = Prjct.objects.get(name=request.POST.get('prjct')) if request.POST.get('type') == 'I' else None
                    legal_entity.code = request.POST.get('code')
                    legal_entity.deposit_bank = request.POST.get('deposit_bank')
                    legal_entity.deposit_bank_account = request.POST.get('deposit_bank_account')
                    legal_entity.tax_number = request.POST.get('tax_number')
                    legal_entity.reg_addr = request.POST.get('reg_addr')
                    legal_entity.reg_phone = request.POST.get('reg_phone')
                    legal_entity.postal_addr = request.POST.get('postal_addr')

                    legal_entity = LegalEntity.objects.create(
                        name=request.POST.get('name'),
                        type=request.POST.get('type'),
                        prjct=Prjct.objects.get(name=request.POST.get('prjct')) if request.POST.get('type') == 'I' else None,
                        code = request.POST.get('code'),
                        deposit_bank=request.POST.get('deposit_bank'),
                        deposit_bank_account=request.POST.get('deposit_bank_account'),
                        tax_number=request.POST.get('tax_number'),
                        reg_addr=request.POST.get('reg_addr'),
                        reg_phone=request.POST.get('reg_phone'),
                        postal_addr=request.POST.get('postal_addr'),
                    )

                    if request.POST.get('contact') != '':
                        contact = User.objects.get(username=request.POST.get('contact').split("-")[-1].split("@")[0].strip())
                        contact.userprofile.legal_entity = legal_entity
                        contact.userprofile.save()
                    """
                
            except FieldDoesNotExist:
                pass

        ChangeHistory.objects.create(
            on=timezone.now(),
            by=request.user,
            db_table_name=legal_entity._meta.db_table,
            db_table_pk=legal_entity.pk,
            detail=chg_log
            )
        
        # messages.info(request, '1 x new Legal Entity [ ' + request.POST['name'] + ' ] was added')
        # return redirect(to='nanopay:legalentity-detail', pk=legal_entity.pk)

        response = JsonResponse({"name": legal_entity.name})
        return response


@login_required
def jsonResponse_legalEntity_getLst(request):
    if request.method == 'GET':

        legal_entity_lst = {}
        for legal_entity in LegalEntity.objects.all():
            legal_entity_lst[legal_entity.name] = legal_entity.pk
        
        # legal_entity_lst = serializers.serialize("json", LegalEntity.objects.all(), fields=["name", "pk"])

        prjct_lst = {}
        for prjct in Prjct.objects.all():
            prjct_lst[prjct.name] = prjct.pk

        # prjct_lst = serializers.serialize("json", Prjct.objects.all(), fields=["name", "pk"])

        external_contact_lst = {}
        for external_contact in User.objects.exclude(email__icontains='tishmanspeyer.com'):
            if  external_contact.username != 'admin' and not 'tishmanspeyer.com' in external_contact.email.lower():
                if hasattr(external_contact, "userprofile"):
                    if not external_contact.userprofile.legal_entity:
                        external_contact_lst['%s - %s' % (external_contact.get_full_name(), external_contact.email)] = external_contact.pk
                else:
                    external_contact_lst['%s - %s' % (external_contact.get_full_name(), external_contact.email)] = external_contact.pk

        legal_entity = {}
        if request.GET.get('legalEntityPk'):
            legalEntity_selected = LegalEntity.objects.get(pk=request.GET.get('legalEntityPk'))
            legal_entity['pk'] = legalEntity_selected.pk
            legal_entity['name'] = legalEntity_selected.name
            legal_entity['type'] = legalEntity_selected.type
            legal_entity['code'] = legalEntity_selected.code
            legal_entity['prjct'] = legalEntity_selected.prjct.name if legalEntity_selected.prjct else ''
            legal_entity['deposit_bank'] = legalEntity_selected.deposit_bank
            legal_entity['deposit_bank_account'] = legalEntity_selected.deposit_bank_account
            legal_entity['tax_number'] = legalEntity_selected.tax_number
            legal_entity['reg_addr'] = legalEntity_selected.reg_addr
            legal_entity['reg_phone'] = legalEntity_selected.reg_phone
            legal_entity['postal_addr'] = legalEntity_selected.postal_addr

            user_profiles = UserProfile.objects.filter(legal_entity=legalEntity_selected)
            for user_profile in user_profiles:
                legal_entity['contact'] = user_profile.user.get_full_name()

            # legal_entity = serializers.serialize("json", LegalEntity.objects.filter(pk=request.GET.get('legalEntityPk')))

        response = [legal_entity, legal_entity_lst, prjct_lst, external_contact_lst]
        return JsonResponse(response, safe=False)
