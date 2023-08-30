from django.core.mail import EmailMessage

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.urls import reverse
from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import get_template

from .models import ModelType, Instance, branchSite, disposalRequest, ScrapRequest
from nanopay.models import Contract
from nanobase.models import ChangeHistory, SubCategory


# --- disposing ---

@login_required
def disposal_request_approve(request):
    if request.method == 'POST':
        disposal_request_pk = request.POST.get('disposalRequestPk').strip()

        disposal_request = get_object_or_404(disposalRequest, pk=disposal_request_pk)
        disposal_request.status = 'A'
        disposal_request.approved_by = request.user
        disposal_request.approved_on = timezone.now()

        disposal_request.save()

        updated_instance_lst = {}
        for dispoasedInstance in disposal_request.instance_set.all():
            if disposal_request.type == 'S':
                dispoasedInstance.status = 'SCRAPPED'
                detail = 'Scrapping request was Approved'
            elif disposal_request.type == 'R':
                dispoasedInstance.status = 'reUSE'
                detail = 'Reusing request was Approved'
            elif dispoasedInstance.type == 'B':
                dispoasedInstance.status = 'buyBACK'
                detail = 'Buy-back request was Approved'
                
            dispoasedInstance.save()

            ChangeHistory.objects.create(
                on=timezone.now(),
                by=request.user,
                db_table_name=dispoasedInstance._meta.db_table,
                db_table_pk=dispoasedInstance.pk,
                detail=detail
                )

            updated_instance_lst[dispoasedInstance.pk] = dispoasedInstance.status

        IT_reviewer_emails = []
        for reviewer in User.objects.filter(groups__name='IT Reviewer'):
            IT_reviewer_emails.append(reviewer.email)

        message = get_template("nanoassets/instance_disposal_request_approve_email.html").render({
            'protocol': 'http',
            'domain': '127.0.0.1:8000',
            # 'instances': request.POST.getlist('instance'),
            'disposal_request': disposal_request,
        })
        mail = EmailMessage(
            subject='ITS express - Please notice - Disposal request was Approved by ' + disposal_request.approved_by.get_full_name(),
            body=message,
            from_email='nanoMessenger <do-not-reply@tishmanspeyer.com>',
            to=[disposal_request.requested_by.email],
            cc=IT_reviewer_emails,
            # reply_to=[EMAIL_ADMIN],
            # connection=
        )
        mail.content_subtype = "html"
        mail.send()
        messages.success(request, "the notification email with Approval decision was sent.")

        # return redirect('nanoassets:instance-disposal-request-list')
        # response = JsonResponse({"url_redirect": reverse("nanoassets:instance-disposal-request-list")})
        response = JsonResponse(updated_instance_lst)
        return response


@login_required
def disposal_request(request):
    if request.method == 'POST':
        instance_selected_pk = request.POST.get('instanceSelectedPk').split(',')
        bulkUpdModalInputValue = request.POST.get('bulkUpdModalInputValue').strip().split(",")[0].strip()
        if bulkUpdModalInputValue == 'Scraping':
            type = 'S'
            detail='Scraping requested'
        elif bulkUpdModalInputValue == 'Reusing':
            type = 'R'
            detail='Reusing requested'
        elif bulkUpdModalInputValue == 'Buying back':
            type = 'B'
            detail='Buying back requested'

        new_req = disposalRequest.objects.create(
                type=type,
                requested_by=request.user
                )
        new_req.save()
        
        updated_instance_lst = {}
        for index, pk in enumerate(instance_selected_pk):
            selected_instance = get_object_or_404(Instance, pk=pk)
            selected_instance.disposal_request = new_req
            selected_instance.save()

            ChangeHistory.objects.create(
                on=timezone.now(),
                by=request.user,
                db_table_name=selected_instance._meta.db_table,
                db_table_pk=selected_instance.pk,
                detail=detail
                )

            updated_instance_lst[pk] = index

        if new_req:
            IT_reviewer_emails = []
            for reviewer in User.objects.filter(groups__name='IT Reviewer'):
                IT_reviewer_emails.append(reviewer.email)

            message = get_template("nanoassets/instance_disposal_request_email.html").render({
                'protocol': 'http',
                'domain': '127.0.0.1:8000',
                'new_req': new_req,
            })
            mail = EmailMessage(
                subject='ITS express - Please approve - IT assets disposal requested by ' + new_req.requested_by.get_full_name(),
                body=message,
                from_email='nanoMessenger <do-not-reply@tishmanspeyer.com>',
                to=IT_reviewer_emails,
                cc=[request.user.email],
                # reply_to=[EMAIL_ADMIN],
                # connection=
            )
            mail.content_subtype = "html"
            mail.send()
            messages.success(request, "the notification email with the request detail is sent")

            response = JsonResponse(updated_instance_lst)
            return response
            # return redirect('nanoassets:instance-disposal-request-list')


@login_required
def jsonResponse_disposal_lst(request):
    if request.method == 'GET':
        chk_lst = {}
        selected_instances_pk = tuple(request.GET.get('instanceSelectedPk').split(','))
        for index, pk in enumerate(selected_instances_pk):
            selected_instance = Instance.objects.get(pk=pk)
            if selected_instance.disposal_request:
                chk_lst[selected_instance.pk] = 'disposalRequested'
            else:
                chk_lst[selected_instance.pk] = selected_instance.status

        opt_lst = {}
        opt_lst['Scraping'] = 'SCRAPPED'
        opt_lst['Reusing'] = 'reUSE'
        opt_lst['Buying back'] = 'buyBACK'

        response = [opt_lst, chk_lst]
        return JsonResponse(response, safe=False)


# --- in Repairing ---

@login_required
def in_repair(request):
    if request.method == 'POST':
        instance_selected_pk = request.POST.get('instanceSelectedPk').split(',')
        instanceSelectedStatus = request.POST.get('instanceSelectedStatus')
        updated_instance_lst = {}
        for index, pk in enumerate(instance_selected_pk):
            selected_instance = get_object_or_404(Instance, pk=pk)

            if instanceSelectedStatus == 'inREPAIR':
                change_history_detail = 'Sent for repairing'
            else:
                change_history_detail = 'Got back from repairing'
            
            ChangeHistory.objects.create(
                on=timezone.now(),
                by=request.user,
                db_table_name=selected_instance._meta.db_table,
                db_table_pk=selected_instance.pk,
                detail=change_history_detail
                )
            selected_instance.status = request.POST.get('instanceSelectedStatus')
            selected_instance.save()

            updated_instance_lst[pk] = instanceSelectedStatus

        response = JsonResponse(updated_instance_lst)
        return response


# --- model / type Changing to ---

@login_required
def jsonResponse_model_type_lst(request):
    if request.method == 'GET':
        chk_lst = {}
        selected_instances_pk = tuple(request.GET.get('instanceSelectedPk').split(','))
        for index, pk in enumerate(selected_instances_pk):
            selected_instance = Instance.objects.get(pk=pk)
            if selected_instance.model_type:
                model_type = selected_instance.model_type
                chk_lst[model_type.name] = model_type.pk
            else:
                chk_lst[''] = selected_instance.pk

        model_types = ModelType.objects.all()
        opt_lst = {}
        for model_type in model_types:
            if not model_type.name in chk_lst:
                if model_type.manufacturer:
                    opt_lst['%s, %s' % (model_type.name, model_type.manufacturer.name)] = model_type.pk
                else:
                    opt_lst[model_type.name] = model_type.pk

        response = [opt_lst, chk_lst]
        return JsonResponse(response, safe=False)


@login_required
def model_type_changing_to(request):
    if request.method == 'POST':
        instance_selected_pk = request.POST.get('instanceSelectedPk').split(',')
        try:
            bulkUpdModalInputValue = request.POST.get('bulkUpdModalInputValue').strip().split(",")[0].strip()
            # model_type_changed_to = ModelType.objects.get(name=request.POST['bulkUpdModalInputValue'])
            model_type_changed_to = ModelType.objects.get(name=bulkUpdModalInputValue)
        except (KeyError, SubCategory.DoesNotExist):
            messages.info(request, 'the Model / Type given is invalid')
            response = JsonResponse({'Error': 'the Model / Type given is invalid'})
        else:
            updated_instance_lst = {}
            for index, pk in enumerate(instance_selected_pk):
                selected_instance = get_object_or_404(Instance, pk=pk)
                
                ChangeHistory.objects.create(
                    on=timezone.now(),
                    by=request.user,
                    db_table_name=selected_instance._meta.db_table,
                    db_table_pk=selected_instance.pk,
                    detail='Model / Type was changed to [ ' + model_type_changed_to.name + ' ] from [ ' + selected_instance.model_type.name + ' ]'
                    )
                updated_instance_lst[pk] = index
                selected_instance.model_type = model_type_changed_to
                selected_instance.save()

            # messages.info(request, 'the selected IT Assets were Transferred to ' + model_type_changed_to.name)
            response = JsonResponse(updated_instance_lst)
            
        return response


# --- Re-sub-categorizing to ---

@login_required
def jsonResponse_sub_category_lst(request):
    if request.method == 'GET':
        chk_lst = {}
        selected_instances_pk = tuple(request.GET.get('instanceSelectedPk').split(','))
        for index, pk in enumerate(selected_instances_pk):
            selected_instance = Instance.objects.get(pk=pk)
            if selected_instance.model_type and selected_instance.model_type.sub_category:
                sub_category = selected_instance.model_type.sub_category
                chk_lst[sub_category.name] = sub_category.pk
            else:
                chk_lst[''] = selected_instance.pk

        sub_categories = SubCategory.objects.all()
        opt_lst = {}
        for sub_category in sub_categories:
            if not sub_category.name in chk_lst:
                opt_lst[sub_category.name] = sub_category.pk

        response = [opt_lst, chk_lst]
        return JsonResponse(response, safe=False)


@login_required
def re_subcategorizing_to(request):
    if request.method == 'POST':
        instance_selected_pk = request.POST.get('instanceSelectedPk').split(',')
        try:
            re_subcategorized_to = SubCategory.objects.get(name=request.POST['bulkUpdModalInputValue'])
        except (KeyError, SubCategory.DoesNotExist):
            messages.info(request, 'the Sub-Category given is invalid')
            response = JsonResponse({'Error': 'the Sub-Category given is invalid'})
        else:
            updated_instance_lst = {}
            for index, pk in enumerate(instance_selected_pk):
                selected_instance = get_object_or_404(Instance, pk=pk)
                
                ChangeHistory.objects.create(
                    on=timezone.now(),
                    by=request.user,
                    db_table_name=selected_instance._meta.db_table,
                    db_table_pk=selected_instance.pk,
                    detail='Model Type of this IT Assets was re-sub-categorized to [ ' + re_subcategorized_to.name + ' ] from [ ' + str(selected_instance.model_type.sub_category) + ' ]'
                    )
                updated_instance_lst[pk] = index
                selected_instance.model_type.sub_category = re_subcategorized_to
                selected_instance.model_type.save()

            # messages.info(request, 'Model Type of this IT Assets was re-sub-categorized to ' + re_subcategorized_to.name)
            response = JsonResponse(updated_instance_lst)
            
        return response


# --- owner Re-assigning to ---

@login_required
def jsonResponse_owner_lst(request):
    if request.method == 'GET':
        chk_lst = {}
        selected_instances_pk = tuple(request.GET.get('instanceSelectedPk').split(','))
        for index, pk in enumerate(selected_instances_pk):
            selected_instance = Instance.objects.get(pk=pk)
            if selected_instance.owner:
                owner = selected_instance.owner
                chk_lst[owner.username] = owner.pk
            else:
                chk_lst[''] = selected_instance.pk

        owners = User.objects.filter(email__icontains='tishmanspeyer')
        opt_lst = {}
        for owner in owners:
            if not owner.username in chk_lst:
                opt_lst['%s ( %s )' % (owner.get_full_name(), owner.username)] = owner.pk
        opt_lst[''] = ''

        response = [opt_lst, chk_lst]
        return JsonResponse(response, safe=False)


@login_required
def owner_re_assigning_to(request):
    if request.method == 'POST':
        instance_selected_pk = request.POST.get('instanceSelectedPk').split(',')
        owner_re_assigned_to = request.POST.get('bulkUpdModalInputValue').strip(")").split("(")[-1].strip()
        owner_re_assigned_to = get_object_or_404(User, username=owner_re_assigned_to) if owner_re_assigned_to != '' else owner_re_assigned_to
        updated_instance_lst = {}
        for index, pk in enumerate(instance_selected_pk):
            selected_instance = get_object_or_404(Instance, pk=pk)
            if owner_re_assigned_to == '' and selected_instance.owner:
                change_history_detail = 'Returned from [ ' + selected_instance.owner.get_full_name() + ' ]'
                # msg = 'the IT Asset(s) [ ' + selected_instance.serial_number + ' ] was Returned from ' + selected_instance.owner.get_full_name()

                selected_instance.status = 'AVAILABLE'
                selected_instance.owner = None

            elif owner_re_assigned_to != '' and owner_re_assigned_to != selected_instance.owner:
                change_history_detail = 'Re-assigned to [ ' + owner_re_assigned_to.get_full_name() + ' ] from [ ' + (selected_instance.owner.get_full_name() if selected_instance.owner else ' 🈳 ') + ' ]'
                # msg = 'the IT Asset(s) [ ' + selected_instance.serial_number + ' ] was Re-assigned to [ ' + owner_re_assigned_to.get_full_name() + ' ] from [ ' + (selected_instance.owner.get_full_name() if selected_instance.owner else ' 🈳 ') + ' ]'

                selected_instance.status = 'inUSE'
                selected_instance.owner = owner_re_assigned_to

            ChangeHistory.objects.create(
                on=timezone.now(),
                by=request.user,
                db_table_name=selected_instance._meta.db_table,
                db_table_pk=selected_instance.pk,
                detail=change_history_detail
                )
                
            # messages.info(request, msg)

            selected_instance.save()
            updated_instance_lst[pk] = index

        response = JsonResponse(updated_instance_lst)
        return response


# --- branch site Transferring to ---

@login_required
def jsonResponse_branchSite_lst(request):
    if request.method == 'GET':
        chk_lst = {}
        selected_instances_pk = tuple(request.GET.get('instanceSelectedPk').split(','))
        for index, pk in enumerate(selected_instances_pk):
            selected_instance = Instance.objects.get(pk=pk)
            # for branchSite in selected_instance.branchSite_set.all():
            branch_site = selected_instance.branchSite
            chk_lst[branch_site.name] = branch_site.pk

        branchSites = branchSite.objects.all()
        opt_lst = {}
        for branch_site in branchSites:
            if not branch_site.name in chk_lst:
                opt_lst[branch_site.name] = branch_site.pk

        response = [opt_lst, chk_lst]
        return JsonResponse(response, safe=False)


@login_required
def branchSite_transferring_to(request):
    if request.method == 'POST':
        instance_selected_pk = request.POST.get('instanceSelectedPk').split(',')
        try:
            branchSite_transferred_to = branchSite.objects.get(name=request.POST['bulkUpdModalInputValue'])
        except (KeyError, branchSite.DoesNotExist):
            messages.info(request, 'the Branch Site given is invalid')
            response = JsonResponse({'Error': 'the Branch Site given is invalid'})
        else:
            updated_instance_lst = {}
            for index, pk in enumerate(instance_selected_pk):
                selected_instance = get_object_or_404(Instance, pk=pk)
                
                ChangeHistory.objects.create(
                    on=timezone.now(),
                    by=request.user,
                    db_table_name=selected_instance._meta.db_table,
                    db_table_pk=selected_instance.pk,
                    detail='Transferred to [ ' + branchSite_transferred_to.name + ' ] from [ ' + selected_instance.branchSite.name + ' ]'
                    )
                updated_instance_lst[pk] = index
                selected_instance.branchSite = branchSite_transferred_to
                selected_instance.save()

            # messages.info(request, 'the selected IT Assets were Transferred to ' + branchSite_transferred_to.name)
            response = JsonResponse(updated_instance_lst)
            
        return response


# --- contract Associating with ---

@login_required
def jsonResponse_contract_lst(request):
    if request.method == 'GET':
        chk_lst = {}
        selected_instances_pk = tuple(request.GET.get('instanceSelectedPk').split(','))
        for index, pk in enumerate(selected_instances_pk):
            selected_instance = Instance.objects.get(pk=pk)
            for contract in selected_instance.contract_set.all():
                chk_lst[contract.briefing] = contract.pk

        contracts = Contract.objects.all()
        opt_lst = {}
        for contract in contracts:
            if not contract.briefing in chk_lst:
                opt_lst[contract.briefing] = contract.get_absolute_url()
        
        response = [opt_lst, chk_lst]
        return JsonResponse(response, safe=False)


@login_required
def contract_associating_with(request):
    if request.method == 'POST':
        instance_selected_pk = request.POST.get('instanceSelectedPk').split(',')
        try:
            contract_associated_with = Contract.objects.filter(briefing__icontains=request.POST['bulkUpdModalInputValue']).first()
        except (KeyError, Contract.DoesNotExist):
            messages.info(request, 'the Contract given is invalid')
            response = JsonResponse({'Error': 'the Contract given is invalid'})
        else:
            updated_instance_lst = {}
            for index, pk in enumerate(instance_selected_pk):
                selected_instance = get_object_or_404(Instance, pk=pk)
                
                ChangeHistory.objects.create(
                    on=timezone.now(),
                    by=request.user,
                    db_table_name=selected_instance._meta.db_table,
                    db_table_pk=selected_instance.pk,
                    detail='Associated with [ ' + contract_associated_with.briefing + ' ]'
                    )
                updated_instance_lst[pk] = index
                contract_associated_with.assets.add(selected_instance)
                contract_associated_with.save()

            # messages.info(request, 'the selected IT Assets were Associated with [ ' + contract_associated_with.briefing + ' ]')
            response = JsonResponse(updated_instance_lst)
        
        return response
