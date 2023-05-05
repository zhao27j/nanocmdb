from typing import Any, Dict
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
    fields = "__all__"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parties = []
        for party in LegalEntity.objects.all():
            parties.append(party.name)
        context['parties'] = parties
        return context