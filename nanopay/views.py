import datetime
import pathlib

from typing import Any, Dict

from django.core.files import File

from django.http import FileResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from django.views import generic
from django.views.generic.edit import CreateView

from .models import Contract, PaymentTerm, LegalEntity
from .forms import NewContractForm, NewPaymentTermForm

# Create your views here.

@login_required
def new_payment_term(request, pk):
    contract = get_object_or_404(Contract, pk=pk)
    if request.method == 'POST': # if this is a POST request then process the Form data
        post = request.POST.copy()
        post['contract'] = contract
        form = NewPaymentTermForm(post) # create a form instance and populate it with data from the request (binding):
        # form.save(commit=False)
        if form.is_valid(): # check if the form is valid:
            # process the data in form.cleaned_data as required
            new_payment_term_plan = form.cleaned_data['plan']
            new_payment_term_recurring = form.cleaned_data['recurring']
            if new_payment_term_plan != 'C' and new_payment_term_recurring > 1:
                pay_day = form.cleaned_data['pay_day']
                recurring = 1
                while recurring < new_payment_term_recurring:
                    if new_payment_term_plan == 'M':
                        pay_day += datetime.timedelta(weeks=(4.33333))
                    elif new_payment_term_plan == 'Q':
                        pay_day += datetime.timedelta(weeks=(13))
                    elif new_payment_term_plan == 'S':
                        pay_day += datetime.timedelta(weeks=(26))
                    elif new_payment_term_plan == 'A':
                        pay_day += datetime.timedelta(weeks=(52))
                    
                    PaymentTerm.objects.create(pay_day=pay_day, plan=new_payment_term_plan, recurring=1, amount=form.cleaned_data['amount'], contract=form.cleaned_data['contract'],)
                    recurring += 1

            new_payment_term = form.save()
            new_payment_term.recurring = 1
            new_payment_term.contract = contract

            contract.activityhistory_set.create(
                description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] '
                  + 'one ' + new_payment_term.get_plan_display()
                    + ' Payment Term scheduled on ' + str(new_payment_term.pay_day)
                      + ' in amount ' + str(new_payment_term.amount)
                        + ' was added by ' + request.user.get_full_name()
                )
            
            messages.info(request, str(new_payment_term_recurring) + ' x Payment Terms for the Contract [ ' + contract.briefing + ' ] were added by ' + request.user.get_full_name())

            return redirect('nanopay:contract-detail', pk=pk) # redirect to a new URL:

    else: # if this is a GET (or any other method) create the default form.
        pay_day = contract.startup + datetime.timedelta(weeks=4.33333)
        form = NewPaymentTermForm(initial={
            'pay_day': pay_day, 
            'contract': contract,
            })

    return render(request, 'nanopay/payment_term_new.html', {'form': form,})


@login_required
def contract_detail_scanned_copy(request, pk):
    contract_instance = get_object_or_404(Contract, pk=pk)
    scanned_copy_path = contract_instance.scanned_copy.name
    try:
        scanned_copy = open(scanned_copy_path, 'rb')
        return FileResponse(scanned_copy, content_type='application/pdf')
    except FileNotFoundError:
        raise Http404


@login_required
def new_contract(request):
    if request.method == 'POST': # if this is a POST request then process the Form data
        form = NewContractForm(request.POST, request.FILES) # create a form instance and populate it with data from the request (binding):
        if form.is_valid(): # check if the form is valid:
            # process the data in form.cleaned_data as required
            new_contract = Contract()
            
            new_contract.briefing = form.cleaned_data['briefing']
            
            new_contract.type = form.cleaned_data['type']
            new_contract.startup = form.cleaned_data['startup']
            new_contract.endup = form.cleaned_data['endup']
            new_contract.scanned_copy = form.cleaned_data['scanned_copy']
            new_contract.created_by = request.user
            new_contract.save()

            new_contract.party_a_list.set(form.cleaned_data['party_a_list'])
            new_contract.party_b_list.set(form.cleaned_data['party_b_list'])

            new_contract.activityhistory_set.create(
                description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' + 'the base info was added by ' + request.user.get_full_name()
                )
            
            messages.info(request, 'the base info of the new Contract [ ' + form.cleaned_data['briefing'] + ' ] was added by ' + request.user.get_full_name())


            # return redirect(new_contract.get_absolute_url()) # redirect to a new URL:
            return redirect('nanopay:payment-term-new', pk=new_contract.pk)

    else: # if this is a GET (or any other method) create the default form.
        startup = datetime.date.today()
        endup = datetime.date.today() + datetime.timedelta(weeks=12)
        form = NewContractForm(
            initial={
                'startup': startup,
                'endup': endup,
                })

    return render(request, 'nanopay/contract_new.html', {'form': form,})


class ContractListView(LoginRequiredMixin, generic.ListView):
    model = Contract
    # paginate_by = 10


class ContractDetailView(LoginRequiredMixin, generic.DetailView):
    model = Contract