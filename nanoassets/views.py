from django.shortcuts import render, get_object_or_404, redirect

# from django.http import HttpResponse

from django.contrib import messages
from django.contrib.auth.models import User, Group
# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.conf import settings
# from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.template.loader import get_template
# from django.template import Context

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
            scrappedInstance.status = 'S'
            scrappedInstance.save()

        reviewer_emails = []
        for reviewer in User.objects.filter(groups__name='IT Reviewer'):
            reviewer_emails.append(reviewer.email)

        message = get_template("nanoassets/instance_scrapping_request_approved_email.html").render({
            'protocol': 'http',
            'domain': '127.0.0.1:8000',
            # 'instances': request.POST.getlist('instance'),
            'scrapRequest': scrapRequest,
        })
        mail = EmailMessage(
            subject='Please notice - IT Assets Scrapping Request is approved by ' +
            scrapRequest.approved_by.get_full_name(),
            body=message,
            from_email='nanoNotification <do-not-reply@tishmanspeyer.com>',
            to=[scrapRequest.requested_by.email],
            cc=reviewer_emails,
            # reply_to=[EMAIL_ADMIN],
            # connection=
        )
        mail.content_subtype = "html"
        mail.send()
        messages.success(
            request, "The notification email with the apprival decision is sent.")

        return redirect('instance-scrapping-request-list')


class InstanceScrappingRequestDetailView(LoginRequiredMixin, generic.DetailView):
    model = ScrapRequest
    template_name = 'nanoassets/instance_scrapping_request_detail.html'


class InstanceScrappingRequestListView(LoginRequiredMixin, generic.ListView):
    model = ScrapRequest
    template_name = 'nanoassets/instance_scrapping_request_list.html'
    # paginate_by = 10


def InstanceScrappingRequest(request):
    if request.method == 'POST':
        if request.POST.getlist('instance'):
            for selected_instance_pk in request.POST.getlist('instance'):
                selected_instance = get_object_or_404(
                    Instance, pk=selected_instance_pk)
                if selected_instance.status != 'A' or selected_instance.scrap_request:
                    messages.warning(
                        request, "Only Available and non-requested IT Assets can be selected.")
                    return redirect('instance-list')

            new_scrap_request = ScrapRequest.objects.create(
                requested_by=request.user)
            new_scrap_request.save()

            for selected_instance_pk in request.POST.getlist('instance'):
                selected_instance = get_object_or_404(
                    Instance, pk=selected_instance_pk)
                selected_instance.scrap_request = new_scrap_request
                selected_instance.save()

            reviewer_emails = []
            for reviewer in User.objects.filter(groups__name='IT Reviewer'):
                reviewer_emails.append(reviewer.email)

            message = get_template("nanoassets/instance_scrapping_request_email.html").render({
                'protocol': 'http',
                'domain': '127.0.0.1:8000',
                'new_scrap_request': new_scrap_request,
            })
            mail = EmailMessage(
                subject='Please approve - IT Assets Scrapping Requested by ' +
                new_scrap_request.requested_by.get_full_name(),
                body=message,
                from_email='nanoNotification <do-not-reply@tishmanspeyer.com>',
                to=reviewer_emails,
                cc=[request.user.email],
                # reply_to=[EMAIL_ADMIN],
                # connection=
            )
            mail.content_subtype = "html"
            mail.send()
            messages.success(
                request, "The notification email with the request detail is sent.")

            return redirect('instance-scrapping-request-list')
        else:
            messages.info(request, "No IT Assets were selected.")
            return redirect('instance-list')


class InstanceSearchResultsListView(generic.ListView):
    model = Instance
    template_name = 'nanoassets/instance_search_results.html'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        
        object_list = Instance.objects.filter(
            Q(serial_number__icontains=query) |
            Q(model_type__name__icontains=query) |
            Q(model_type__manufacturer__name__icontains=query) |
            Q(status__icontains=query) |
            Q(owner__username__icontains=query) |
            Q(owner__first_name__icontains=query) |
            Q(owner__last_name__icontains=query) |
            Q(owner__email__icontains=query)
        )
        if object_list:
            messages.info(self.request, "%s results found." %
                        object_list.count())
            return object_list
        else:
            messages.info(self.request, "No results found.")
            # return redirect('instance-list')


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
