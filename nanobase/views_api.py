from django.http import JsonResponse

from django.utils import timezone

from django.shortcuts import get_object_or_404

from django.core.serializers import serialize
from django.core.exceptions import FieldDoesNotExist

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import UserProfile, UserDept, ChangeHistory
from nanopay.models import LegalEntity

@login_required
def user_crud(request):
    if request.method == 'POST':
        # user, user_created = User.objects.get_or_create(name=request.POST.get('email'))
        chg_log = ''
        try:
            user = User.objects.get(email=request.POST.get('email'))
            user_created = False
        except User.DoesNotExist:
            # user = User.objects.create_user()
            user = User.objects.create(
                username=request.POST.get('email').split('@')[0],
            )
            user_created = True

        user_profile, user_profile_created = UserProfile.objects.get_or_create(user=user)

        for k, v in request.POST.copy().items():
            try:
                User._meta.get_field(k)
                if user_created:
                    chg_log = '1 x new User [ ' + user.get_full_name() + ' ] was added'
                    setattr(user, k, v)
                else:
                    if getattr(user, k):
                        from_orig = getattr(user, k)
                        try:
                            User._meta.get_field(k).related_fields
                            from_orig = from_orig.name
                        except AttributeError:
                            pass
                    else: 
                        from_orig = '🈳'
                    to_target = v if v != '' else '🈳'
                    if to_target != from_orig:
                        chg_log += 'The ' + k.capitalize() + ' was changed from [ ' + str(from_orig) + ' ] to [ ' + str(to_target) + ' ]; '
                        setattr(user, k, v)
                
                user.save()
                
            except FieldDoesNotExist:
                try:
                    UserProfile._meta.get_field(k)
                    if not user_created:
                        if getattr(user_profile, k):
                            from_orig = getattr(user_profile, k)
                            try:
                                UserProfile._meta.get_field(k).related_fields
                                from_orig = from_orig.name
                            except AttributeError:
                                pass
                        else: 
                            from_orig = '🈳'

                        to_target = v if v != '' else '🈳'
                        chg_log += 'The ' + k.capitalize() + ' was changed from [ ' + str(from_orig) + ' ] to [ ' + str(to_target) + ' ]; '

                    if k == 'dept' and v != '':
                        dept, dept_created = UserDept.objects.get_or_create(name=v.title())
                        if dept_created:
                            ChangeHistory.objects.create(
                                on=timezone.now(),
                                by=request.user,
                                db_table_name=dept._meta.db_table,
                                db_table_pk=dept.pk,
                                detail='1 x Department is added'
                            )
                        setattr(user_profile, k, dept)
                    elif k == 'legal_entity' and v != '':
                        legal_entity = get_object_or_404(LegalEntity, name=v)
                        setattr(user_profile, k, legal_entity)
                        ChangeHistory.objects.create(
                            on=timezone.now(),
                            by=request.user,
                            db_table_name=legal_entity._meta.db_table,
                            db_table_pk=legal_entity.pk,
                            detail='1 x Contact [ ' + user.get_full_name() + ' ] is added and associated with this Legal Entity'
                        )
                    else:
                        setattr(user_profile, k, v)
                        
                    user_profile.save()
                        
                except FieldDoesNotExist:
                    pass

        ChangeHistory.objects.create(
            on=timezone.now(),
            by=request.user,
            db_table_name=user_profile._meta.db_table,
            db_table_pk=user_profile.pk,
            detail=chg_log
            )
        
        response = JsonResponse({"chg_log": chg_log})
        return response


@login_required
def jsonResponse_user_getLst(request):
    if request.method == 'GET':
        user_selected = {}
        if request.GET.get('userPk'):
            userSelected = User.objects.get(pk=request.GET.get('userPk'))
            user_selected['username'] = userSelected.username
            user_selected['first_name'] = userSelected.first_name
            user_selected['last_name'] = userSelected.last_name
            user_selected['email'] = userSelected.email
            try:
                userSelected.userprofile
            except User.userprofile.RelatedObjectDoesNotExist:
                userSelected.save()

            user_selected['title'] = userSelected.userprofile.title if userSelected.userprofile.title != None else ''
            user_selected['dept'] = userSelected.userprofile.dept.name if userSelected.userprofile.dept else ''
            user_selected['cellphone'] = userSelected.userprofile.cellphone if userSelected.userprofile.cellphone != None else ''
            user_selected['work_phone'] = userSelected.userprofile.work_phone if userSelected.userprofile.work_phone != None else ''
            user_selected['postal_addr'] = userSelected.userprofile.postal_addr if userSelected.userprofile.postal_addr != None else ''
            user_selected['legal_entity'] = userSelected.userprofile.legal_entity.name if userSelected.userprofile.legal_entity else ''

        legal_entity_selected = {}
        if request.GET.get('legalEntityPk'):
            legalEntitySelected = LegalEntity.objects.get(pk=request.GET.get('legalEntityPk'))
            legal_entity_selected['pk'] = legalEntitySelected.pk
            legal_entity_selected['name'] = legalEntitySelected.name

            legal_entity_selected['email_domain'] = legalEntitySelected.userprofile_set.all().first().user.email.split('@')[1]

        dept_lst = {}
        for user_dept in UserDept.objects.all():
            dept_lst[user_dept.name] = user_dept.pk

        legal_entity_lst = {}
        for legal_entity in LegalEntity.objects.all():
            if legal_entity.type == 'E':
                legal_entity_lst[legal_entity.name] = legal_entity.pk

        user_email_lst = {}
        for user in User.objects.all():
            user_email_lst[user.email] = user.pk

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
            # legal_entity = serializers.serialize("json", LegalEntity.objects.filter(pk=request.GET.get('legalEntityPk')))

        response = [dept_lst, legal_entity_lst, user_email_lst, legal_entity_selected, user_selected, ]
        return JsonResponse(response, safe=False)