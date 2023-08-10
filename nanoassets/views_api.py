from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.utils import timezone

from django.http import JsonResponse

from django.shortcuts import get_object_or_404

from .models import Instance, branchSite
from nanopay.models import Contract
from nanobase.models import ChangeHistory


# --- branch site Transferring to ---

@login_required
def jsonResponse_branchSite_lst(request):
    if request.method == 'GET':
        branchSite_associated_with_instance_list = {}
        selected_instances_pk = tuple(request.GET.get('instanceSelectedPkPost').split(','))
        for selected_instances_pk_index, selected_instance_pk in enumerate(selected_instances_pk):
            selected_instance = Instance.objects.get(pk=selected_instance_pk)
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
        selected_instances = request.POST.get('instanceSelectedPkPost').split(',')
        try:
            branchSite_transferred_to = branchSite.objects.get(name=request.POST['branchSite_transferred_to'])
        except (KeyError, branchSite.DoesNotExist):
            messages.info(request, 'the Branch Site given is invalid')
            response = JsonResponse('the Branch Site given is invalid')
        else:
            selected_instance_list = {}
            for selected_instances_pk_index, selected_instance_pk in enumerate(selected_instances):
                selected_instance = get_object_or_404(Instance, pk=selected_instance_pk)
                
                ChangeHistory.objects.create(
                    on=timezone.now(),
                    by=request.user,
                    db_table_name=selected_instance._meta.db_table,
                    db_table_pk=selected_instance.pk,
                    detail='Transferred to [ ' + branchSite_transferred_to.name + ' ] from [ ' + selected_instance.branchSite.name + ' ]'
                    )
                selected_instance_list[selected_instance_pk] = selected_instances_pk_index
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
        selected_instances_pk = tuple(request.GET.get('instanceSelectedPkPost').split(','))
        for selected_instances_pk_index, selected_instance_pk in enumerate(selected_instances_pk):
            selected_instance = Instance.objects.get(pk=selected_instance_pk)
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
        selected_instances = request.POST.get('instanceSelectedPkPost').split(',')
        try:
            contract_associated_with = Contract.objects.filter(briefing__icontains=request.POST['contract_associated_with']).first()
        except (KeyError, Contract.DoesNotExist):
            messages.info(request, 'the Contract given is invalid')
            response = JsonResponse('the Contract given is invalid')
        else:
            selected_instance_list = {}
            for selected_instances_pk_index, selected_instance_pk in enumerate(selected_instances):
                selected_instance = get_object_or_404(Instance, pk=selected_instance_pk)
                
                ChangeHistory.objects.create(
                    on=timezone.now(),
                    by=request.user,
                    db_table_name=selected_instance._meta.db_table,
                    db_table_pk=selected_instance.pk,
                    detail='Associated with [ ' + contract_associated_with.briefing + ' ]'
                    )
                selected_instance_list[selected_instance_pk] = selected_instances_pk_index
                contract_associated_with.assets.add(selected_instance)
                contract_associated_with.save()

            messages.info(request, 'the selected IT Assets were Associated with [ ' + contract_associated_with.briefing + ' ]')
            response = JsonResponse(selected_instance_list)
        
        return response
