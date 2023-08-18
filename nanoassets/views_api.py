from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.utils import timezone
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Instance, branchSite
from nanopay.models import Contract
from nanobase.models import ChangeHistory


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
                # opt_lst[owner.get_full_name()] = owner.pk

        response = [opt_lst, chk_lst]
        return JsonResponse(response, safe=False)


def owner_re_assigning_to(request):
    if request.method == 'POST':
        instance_selected_pk = request.POST.get('instanceSelectedPk').split(',')
        owner_re_assigned_to = request.POST.get('bulkUpdModalInputValue').strip(")").split("(")[-1].strip()
        owner_re_assigned_to = get_object_or_404(User, username=owner_re_assigned_to) if owner_re_assigned_to != '' else owner_re_assigned_to
        selected_instance_list = {}
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
            selected_instance_list[pk] = index

        response = JsonResponse(selected_instance_list)
        return response


# --- branch site Transferring to ---

@login_required
def jsonResponse_branchSite_lst(request):
    if request.method == 'GET':
        branchSite_associated_with_instance_list = {}
        selected_instances_pk = tuple(request.GET.get('instanceSelectedPk').split(','))
        for index, pk in enumerate(selected_instances_pk):
            selected_instance = Instance.objects.get(pk=pk)
            # for branchSite in selected_instance.branchSite_set.all():
            branch_site = selected_instance.branchSite
            branchSite_associated_with_instance_list[branch_site.name] = branch_site.pk

        branchSites = branchSite.objects.all()
        branchSite_opt_list = {}
        for branch_site in branchSites:
            if not branch_site.name in branchSite_associated_with_instance_list:
                branchSite_opt_list[branch_site.name] = branch_site.pk

        response = [branchSite_opt_list, branchSite_associated_with_instance_list]
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
            selected_instance_list = {}
            for index, pk in enumerate(instance_selected_pk):
                selected_instance = get_object_or_404(Instance, pk=pk)
                
                ChangeHistory.objects.create(
                    on=timezone.now(),
                    by=request.user,
                    db_table_name=selected_instance._meta.db_table,
                    db_table_pk=selected_instance.pk,
                    detail='Transferred to [ ' + branchSite_transferred_to.name + ' ] from [ ' + selected_instance.branchSite.name + ' ]'
                    )
                selected_instance_list[pk] = index
                selected_instance.branchSite = branchSite_transferred_to
                selected_instance.save()

            messages.info(request, 'the selected IT Assets were Transferred to ' + branchSite_transferred_to.name)
            response = JsonResponse(selected_instance_list)
            
        return response


# --- contract Associating with ---

@login_required
def jsonResponse_contract_lst(request):
    if request.method == 'GET':
        contract_associated_with_instance_list = {}
        selected_instances_pk = tuple(request.GET.get('instanceSelectedPk').split(','))
        for index, pk in enumerate(selected_instances_pk):
            selected_instance = Instance.objects.get(pk=pk)
            for contract in selected_instance.contract_set.all():
                contract_associated_with_instance_list[contract.briefing] = contract.pk

        contracts = Contract.objects.all()
        contract_opt_list = {}
        for contract in contracts:
            if not contract.briefing in contract_associated_with_instance_list:
                contract_opt_list[contract.briefing] = contract.get_absolute_url()
        
        response = [contract_opt_list, contract_associated_with_instance_list]
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
            selected_instance_list = {}
            for index, pk in enumerate(instance_selected_pk):
                selected_instance = get_object_or_404(Instance, pk=pk)
                
                ChangeHistory.objects.create(
                    on=timezone.now(),
                    by=request.user,
                    db_table_name=selected_instance._meta.db_table,
                    db_table_pk=selected_instance.pk,
                    detail='Associated with [ ' + contract_associated_with.briefing + ' ]'
                    )
                selected_instance_list[pk] = index
                contract_associated_with.assets.add(selected_instance)
                contract_associated_with.save()

            messages.info(request, 'the selected IT Assets were Associated with [ ' + contract_associated_with.briefing + ' ]')
            response = JsonResponse(selected_instance_list)
        
        return response
