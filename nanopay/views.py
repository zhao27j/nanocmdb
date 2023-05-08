from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.views.generic.edit import CreateView

from .models import Contract, LegalEntity

# Create your views here.

class ContractListView(LoginRequiredMixin, generic.ListView):
    model = Contract
    # paginate_by = 10


class ContractDetailView(LoginRequiredMixin, generic.DetailView):
    model = Contract


class ContractCreateView(LoginRequiredMixin, CreateView):
    model = Contract
    fields = ["briefing"] # fields = "__all__"
    # template_name = 'nanopay/contract_form copy.html'
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

        return super().form_valid(form)

    """
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            pass
        return super().post(request, *args, **kwargs)
    """