import datetime

from typing import Any, Dict

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import generic
from django.views.generic.edit import CreateView

from .models import Contract, LegalEntity
from .forms import NewContractForm

# Create your views here.

def new_contract(request):
    
    if request.method == 'POST': # if this is a POST request then process the Form data
        new_contract=Contract.objects.create()

        form = NewContractForm(request.POST) # create a form instance and populate it with data from the request (binding):

        if form.is_valid(): # check if the form is valid:
            # process the data in form.cleaned_data as required
            new_contract = form.clean()
            
            new_contract.save()

            return HttpResponseRedirect(reverse('nanopay:contract-detail new_contract.pk') ) # redirect to a new URL:

    else: # if this is a GET (or any other method) create the default form.
        startup = datetime.date.today()
        endup = datetime.date.today() + datetime.timedelta(weeks=12)
        form = NewContractForm(
            initial={
                'startup': startup,
                'endup': endup,
                })

    return render(request, 'nanopay/contract_form_new.html', {
        'form': form,
        # 'new_contract': new_contract, 
        })


class ContractListView(LoginRequiredMixin, generic.ListView):
    model = Contract
    # paginate_by = 10


class ContractDetailView(LoginRequiredMixin, generic.DetailView):
    model = Contract


class ContractCreateView(LoginRequiredMixin, CreateView):
    model = Contract
    # fields = ["briefing",] # 
    fields = "__all__"
    template_name = 'nanopay/contract_form copy.html'
    success_url = reverse_lazy('nanopay:contract-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parties_internal = []
        parties_external = []
        for party in LegalEntity.objects.filter(type__icontains='I'):
            parties_internal.append(party.name)
        context['parties_internal'] = parties_internal
        for party in LegalEntity.objects.filter(type__icontains='E'):
            parties_external.append(party.name)
        context['parties_external'] = parties_external
        return context
    
    def form_valid(self, form):
        startup = datetime.strptime(self.request.POST['startup'], '%Y-%m-%d').date()
        endup = datetime.strptime(self.request.POST['endup'], '%Y-%m-%d').date()

        if endup < startup:
            messages.warning(
                self.request, "The End date should not be later than the Start date"
            )
            return redirect(self.request.path) # 重定向 至 当前 页面
        
        return super().form_valid(form)

    
    def post(self, request, *args, **kwargs):
        
        # form = self.form_class(request.POST)
        form = self.get_form()
        if form.is_valid():
            form.save(commit=False)
            form.instance.briefing = self.request.POST['briefing']
            contract_instance = form.save()
            form.save_m2m()
            # party_a_list = self.request.POST.getlist('party_a_list')
            for party_a in self.request.POST.getlist('party_a_list'):
                # form.save_m2m()
                form.instance.party_a_list.add(LegalEntity.objects.get(name=party_a))
                

            # form.instance.party_b_list.add(self.request.POST['party_b_list']) # form.instance.party_b_list.add = self.request.POST['party_b_list']
            form.instance.type = self.request.POST['type']
            form.instance.startup = self.request.POST['startup']
            form.instance.endup = self.request.POST['endup']

        return super().post(request, *args, **kwargs)

        # return redirect('nanopay:contract-list')

