from django.shortcuts import render, get_object_or_404, redirect

from django.http import HttpResponse

from django.contrib.auth.models import User
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils import timezone

from django.db.models import Q

from .models import Instance, ModelType, Manufacturer, ScrapRequest

# Create your views here.


def InstanceScrappingRequestApproved(request, pk):
    if request.method == 'POST':
        scrapRequest = get_object_or_404(ScrapRequest, pk=pk)
        scrapRequest.status = 'A'
        scrapRequest.approved_by = request.user
        scrapRequest.approved_on = timezone.now()
        scrapRequest.save()

        for scrappedInstance in scrapRequest.instance_set.all():
            scrappedInstance.status = 'Disposal'
            scrappedInstance.save()

    return redirect('instance-scrapping-request-list')


class InstanceScrappingRequestDetailView(generic.DetailView):
    model = ScrapRequest
    template_name = 'nanoassets/instance_scrapping_request_detail.html'


class InstanceScrappingRequestListView(LoginRequiredMixin, generic.ListView):
    model = ScrapRequest
    template_name = 'nanoassets/instance_scrapping_request_list.html'
    # paginate_by = 10


def InstanceScrappingRequest(request):
    if request.method == 'POST':

        new_scrap_request = ScrapRequest.objects.create(
            requested_by=request.user)
        new_scrap_request.save()

        for selected_instance_pk in request.POST.getlist('instance'):
            selected_instance = get_object_or_404(
                Instance, pk=selected_instance_pk)
            selected_instance.scrap_request = new_scrap_request
            selected_instance.save()

        return redirect('instance-scrapping-request-list')


class InstanceSearchResultsListView(generic.ListView):
    model = Instance
    template_name = 'nanoassets/instance_search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Instance.objects.filter(
            Q(serial_number__icontains=query) | Q(status__icontains=query) | Q(owner__username__icontains=query) | Q(
                model_type__name__icontains=query) | Q(model_type__manufacturer__name__icontains=query)
        )
        return object_list


class InstanceCreate(CreateView):
    model = Instance
    fields = '__all__'


class InstanceModelTypeUpdate(UpdateView):
    model = Instance
    # fields = '__all__'
    fields = ['model_type']
    template_name = 'nanoassets/instance_update_modeltype.html'
    success_url = reverse_lazy('instance-list')


class InstanceStatusUpdate(UpdateView):
    model = Instance
    # fields = '__all__'
    fields = ['status']
    template_name = 'nanoassets/instance_update_status.html'
    success_url = reverse_lazy('instance-list')


class InstanceDetailView(generic.DetailView):
    model = Instance


class InstanceByUserListView(LoginRequiredMixin, generic.ListView):
    model = Instance
    template_name = 'nanoassets/instance_list_by_user.html'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user).filter(status__exact='U').order_by('eol_date')
        # return Instance.objects.filter(owner=self.request.user).filter(status__exact='u').order_by('eol_date')


class InstanceListView(LoginRequiredMixin, generic.ListView):
    model = Instance
    paginate_by = 10


class ModelTypeDelete(DeleteView):
    model = ModelType
    success_url = reverse_lazy("modeltype-list")


class ModelTypeUpdate(UpdateView):
    model = ModelType
    fields = '__all__'


class ModelTypeCreate(CreateView):
    model = ModelType
    fields = '__all__'


class ModelTypeDetailView(generic.DetailView):
    model = ModelType


class ModelTypeListView(generic.ListView):
    model = ModelType
    paginate_by = 10


def index(request):
    return render(request, "index.html", {})
