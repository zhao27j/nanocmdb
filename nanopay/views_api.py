
from django.utils import timezone

from django.http import JsonResponse

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import LegalEntity, Prjct
from nanobase.models import ChangeHistory


@login_required
def legal_entity_new(request):
    if request.method == 'POST':
        new_legal_entity = LegalEntity.objects.create(
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
            contact.userprofile.legal_entity = new_legal_entity
            contact.userprofile.save()

        ChangeHistory.objects.create(
            on=timezone.now(),
            by=request.user,
            db_table_name=new_legal_entity._meta.db_table,
            db_table_pk=new_legal_entity.pk,
            detail='1 x new Legal Entity [ ' + new_legal_entity.name + ' ] was added'
            )
        
        # messages.info(request, '1 x new Legal Entity [ ' + request.POST['name'] + ' ] was added')
        # return redirect(to='nanopay:legalentity-detail', pk=new_legal_entity.pk)

        response = JsonResponse({"name": new_legal_entity.name})
        return response


@login_required
def jsonResponse_legal_entity_new_lst(request):
    if request.method == 'GET':
        legal_entity_lst = {}
        for legal_entity in LegalEntity.objects.all():
            legal_entity_lst[legal_entity.name] = legal_entity.pk
        
        prjct_lst = {}
        for prjct in Prjct.objects.all():
            prjct_lst[prjct.name] = prjct.pk

        external_contact_lst = {}
        for external_contact in User.objects.exclude(email__icontains='tishmanspeyer.com'):
            if  external_contact.username != 'admin' and not 'tishmanspeyer.com' in external_contact.email.lower():
                if hasattr(external_contact, "userprofile"):
                    if not external_contact.userprofile.legal_entity:
                        external_contact_lst['%s - %s' % (external_contact.get_full_name(), external_contact.email)] = external_contact.pk
                else:
                    external_contact_lst['%s - %s' % (external_contact.get_full_name(), external_contact.email)] = external_contact.pk

        response = [legal_entity_lst, prjct_lst, external_contact_lst]
        return JsonResponse(response, safe=False)
