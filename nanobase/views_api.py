from django.http import JsonResponse

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import UserProfile, UserDept
from nanoassets.models import Instance
from nanopay.models import LegalEntity


@login_required
def jsonResponse_user_getLst(request):
    if request.method == 'GET':

        dept_lst = {}
        for user_dept in UserDept.objects.all():
            dept_lst[user_dept.name] = user_dept.pk

        legal_entity_lst = {}
        for legal_entity in LegalEntity.objects.all():
            if legal_entity.type == 'E':
                legal_entity_lst[legal_entity.name] = legal_entity.pk

        """
        prjct_lst = {}
        for prjct in Prjct.objects.all():
            prjct_lst[prjct.name] = prjct.pk
        """

        external_contact_lst = {}
        for external_contact in User.objects.exclude(email__icontains='tishmanspeyer.com'):
            if  external_contact.username != 'admin' and not 'tishmanspeyer.com' in external_contact.email.lower():
                if hasattr(external_contact, "userprofile"):
                    if not external_contact.userprofile.legal_entity:
                        external_contact_lst['%s - %s' % (external_contact.get_full_name(), external_contact.email)] = external_contact.pk
                else:
                    external_contact_lst['%s - %s' % (external_contact.get_full_name(), external_contact.email)] = external_contact.pk

        """
        user_picked = {}
        if request.GET.get('userPk'):
            user_picked = User.objects.get(pk=request.GET.get('userPk'))
            

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


            change_history = {}
            changes = ChangeHistory.objects.filter(db_table_name=legalEntity_selected._meta.db_table, db_table_pk=legalEntity_selected.pk).order_by("-on")
            for change in changes:
                change_history[change.detail] = change.by.get_full_name() + str(legalEntity_selected.pk) + change.on.strftime("%Y-%m-%d %H:%M:%S")
        """
            
            # legal_entity = serializers.serialize("json", LegalEntity.objects.filter(pk=request.GET.get('legalEntityPk')))

        response = [dept_lst, legal_entity_lst, external_contact_lst, ]
        return JsonResponse(response, safe=False)


"""
if request.method == 'GET':
    chk_lst = {}
    selected_instances_pk = tuple(request.GET.get('instanceSelectedPk').split(','))
    for index, pk in enumerate(selected_instances_pk):
        selected_instance = Instance.objects.get(pk=pk)
        # for branchSite in selected_instance.branchSite_set.all():
        owner = selected_instance.owner
        chk_lst[owner.username] = owner.pk

    owners = User.objects.filter(email__icontains='tishmanspeyer')
    opt_lst = {}
    for owner in owners:
        if not owner.username in chk_lst:
            opt_lst['%s ( %s )' % (owner.get_full_name(), owner.username)] = owner.pk
            # opt_lst[owner.get_full_name()] = owner.pk

    response = [opt_lst, chk_lst]
    return JsonResponse(response, safe=False)
"""