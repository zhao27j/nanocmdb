
import json
from decimal import Decimal

from django.utils import timezone

from django.core.exceptions import FieldDoesNotExist
from django.core.serializers import serialize
from django.core.mail import EmailMessage

from django.http import JsonResponse
from django.template.loader import get_template

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Contract, LegalEntity, Prjct, NonPayrollExpense
from nanobase.models import UserProfile, ChangeHistory

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super(DecimalEncoder, self).default(obj)


@login_required
def jsonResponse_nonPayrollExpense_getLst(request):
    if request.method == 'GET':
        nonPayrollExpense_budgetYears = list(set(NonPayrollExpense.objects.values_list('non_payroll_expense_year', flat=True).distinct()))

        nonPayrollExpenses_by_budgetYear = NonPayrollExpense.objects.filter(non_payroll_expense_year=int(request.GET.get('budgetYear')))
        response = [json.loads(serialize("json", nonPayrollExpenses_by_budgetYear)), json.dumps(nonPayrollExpense_budgetYears, cls=DecimalEncoder)]

        return JsonResponse(response, safe=False)

@login_required
def contract_mail_me_the_assets_list(request):
    if request.method == 'GET':
        contract = Contract.objects.get(pk=request.GET.get('contractPk'))
        instances = contract.assets.none()
        if request.GET.get('instancesPk'):
            instances_selected_pk = request.GET.get('instancesPk').strip(',').split(',')
            for pk in instances_selected_pk:
                instance = contract.assets.filter(pk=pk)
                instances = instances | instance
        else:
            instances = contract.assets.all()
        
        message = get_template("nanopay/contract_mail_me_the_assets_list.html").render({
                'protocol': 'http',
                'domain': '127.0.0.1:8000',
                'contract': contract,
                'instances': instances,
                'by': request.user.get_full_name(),
                'on': timezone.now(),
        })
        mail = EmailMessage(
            subject='ITS express - IT asset list of ' + contract.briefing,
            body=message,
            from_email='nanoMessenger <do-not-reply@tishmanspeyer.com>',
            to=[request.user.email, ],
            # cc=[request.user.email],
            # reply_to=[EMAIL_ADMIN],
            # connection=
        )
        mail.content_subtype = "html"
        is_sent = mail.send()
        if is_sent:
            messages.success(request, "the asset list of " + contract.briefing + " was successfully sent")
            response = JsonResponse({'is_sent': contract.briefing})
        else:
            messages.success(request, "the asset list of " + contract.briefing + " was NOT sent dur to some errors")
            response = JsonResponse({'is_sent': False})

        return response


@login_required
def jsonResponse_legalEntities_getLst(request):
    if request.method == 'GET':
        legal_entities = LegalEntity.objects.all().order_by("type", "prjct")

        legal_entity_types = {}
        legal_entity_prjcts = {}
        legal_entity_contacts = {}
        for legal_entity in legal_entities:
            legal_entity_types[legal_entity.type] = legal_entity.get_type_display()
            
            if legal_entity.prjct:
                legal_entity_prjcts[legal_entity.prjct.pk] = legal_entity.prjct.name

            if legal_entity.userprofile_set.all():
                legal_entity_contacts[legal_entity.pk] = True

        # num_of_prjct = legal_entities.values('prjct').distinct().count()
        # num_of_type = legal_entities.values('type').distinct().count()

        response = [json.loads(serialize("json", legal_entities)), legal_entity_types, legal_entity_prjcts, legal_entity_contacts]

        return JsonResponse(response, safe=False)


@login_required
def legal_entity(request):
    if request.method == 'POST':
        # legal_entity, created = LegalEntity.objects.get_or_create(name=request.POST.get('name'))
        chg_log = ''
        try:
            legal_entity = LegalEntity.objects.get(pk=request.POST.get('pk'))
            created = False
        except LegalEntity.DoesNotExist:
            legal_entity = LegalEntity.objects.create()
            created = True

        for k, v in request.POST.copy().items():
            try:
                LegalEntity._meta.get_field(k)

                if created:
                    chg_log = '1 x new Legal Entity [ ' + legal_entity.name + ' ] was added'
                else:
                    if getattr(legal_entity, k):
                        from_orig = getattr(legal_entity, k)
                        try:
                            LegalEntity._meta.get_field(k).related_fields
                            from_orig = from_orig.name
                        except AttributeError:
                            pass
                    else: 
                        from_orig = '🈳'
                    to_target = v if v != '' else '🈳'
                    chg_log += 'The ' + k.capitalize() + ' was changed from [ ' + from_orig + ' ] to [ ' + to_target + ' ]; '

                if k == 'prjct':
                    if request.POST.get('type') == 'I':
                        legal_entity.prjct = Prjct.objects.get(name=v) 
                    else:
                        legal_entity.prjct = None
                else:
                    setattr(legal_entity, k, v)

                legal_entity.save()
                
            except FieldDoesNotExist:
                pass

            if k == 'contact' and v != '':
                contact = User.objects.get(username=request.POST.get('contact').split("-")[-1].split("@")[0].strip())
                if UserProfile.objects.filter(user=contact).exists():
                    contact.userprofile.legal_entity = legal_entity
                    contact.userprofile.save()
                else:
                    UserProfile.objects.create(user=contact, legal_entity=legal_entity)
            elif k == 'contact' and v == '':
                try:
                    user_profiles = UserProfile.objects.filter(legal_entity=legal_entity)
                    for user_profile in user_profiles:
                        user_profile.legal_entity = None
                        user_profile.save()
                except UserProfile.DoesNotExist:
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

        # response = JsonResponse({"name": legal_entity.name})

        # chg_log = "<a href="{% url 'nanopay:legalentity-detail' legal_entity.pk %}" class="text-decoration-none"><small>{{ legal_entity.name }}</small></a>"
        response = JsonResponse({"chg_log": chg_log})
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

            """
            change_history = {}
            changes = ChangeHistory.objects.filter(db_table_name=legalEntity_selected._meta.db_table, db_table_pk=legalEntity_selected.pk).order_by("-on")
            for change in changes:
                change_history[change.detail] = change.by.get_full_name() + str(legalEntity_selected.pk) + change.on.strftime("%Y-%m-%d %H:%M:%S")
            """
            
            # legal_entity = serializers.serialize("json", LegalEntity.objects.filter(pk=request.GET.get('legalEntityPk')))

        response = [legal_entity, legal_entity_lst, prjct_lst, external_contact_lst]
        return JsonResponse(response, safe=False)
