from django.shortcuts import render, get_object_or_404, redirect

# from django.http import HttpResponse, HttpResponseRedirect

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

from .models import Instance, ModelType, Manufacturer, ScrapRequest, branchSite

# Create your views here.


def InstanceScrappingRequestApproved(request, pk):
    if request.method == 'POST':
        scrapRequest = get_object_or_404(ScrapRequest, pk=pk)
        scrapRequest.status = 'AVAILABLE'
        scrapRequest.approved_by = request.user
        scrapRequest.approved_on = timezone.now()
        scrapRequest.save()

        for scrappedInstance in scrapRequest.instance_set.all():
            scrappedInstance.status = 'SCRAPPED'
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
                if selected_instance.status != 'AVAILABLE' or selected_instance.scrap_request:
                    messages.warning(
                        request, "Only Available and non-requested IT Assets can be selected.")
                    # return redirect('supported-instance-list')
                    # return redirect(request.path) # 重定向 至 当前 页面 （在此不适合）
                    # 重定向 至 前一个 页面
                    return redirect(request.META.get('HTTP_REFERER'))

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
            return redirect('supported-instance-list')


class InstanceSearchResultsListView(generic.ListView):
    model = Instance
    template_name = 'nanoassets/instance_search_results.html'
    paginate_by = 5

    def get_queryset(self):
        queries = tuple(self.request.GET.get('q').split(','))
        # query_search = tuple(query.split(','))
        object_list = Instance.objects.filter(branchSite__onSiteTech=self.request.user)

        for query in queries:
            object_list = object_list.filter(
                Q(serial_number__icontains=query) | 
                Q(model_type__name__icontains=query) | 
                Q(model_type__manufacturer__name__icontains=query) | 
                Q(status__icontains=query) | 
                Q(owner__username__icontains=query) | 
                Q(owner__first_name__icontains=query) | 
                Q(owner__last_name__icontains=query) | 
                Q(owner__email__icontains=query) | 
                Q(configuragion__hostname__icontains=query) | 
                Q(branchSite__name__icontains=query) | 
                Q(branchSite__city__name__icontains=query)
                )
            # result_list.append(object_list)

        if object_list:
            messages.info(self.request, "%s results found." %
                          object_list.count())
        else:
            messages.info(self.request, "No results found.")
            # self.request.GET = self.request.GET.copy()
            # self.request.GET['q'] = ''

        return object_list


def InstanceInRepair(request, pk):
    # 测试 组 权限 user.groups.filter(name__in=['group1', 'group2']).exists()
    if request.user.groups.filter(name='IT China').exists:
        instance = get_object_or_404(Instance, pk=pk)
        if instance.status != 'inREPAIR':
            instance.status = 'inREPAIR'
            instance.activityhistory_set.create(
                description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' +
                'Sent to repair by ' + request.user.get_full_name())
            # instance.activityhistory_set.save()
            messages.info(request, instance.serial_number + ' (' +
                          instance.model_type.name + ') ' + "was sent to repair.")
        elif instance.status == 'inREPAIR' and instance.owner:
            instance.status = 'inUSE'
            instance.activityhistory_set.create(
                description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' +
                'Got back from repairing by ' + request.user.get_full_name())
            messages.info(request, instance.serial_number +
                          ' (' + instance.model_type.name + ') ' + "was Repaired.")
        elif instance.status == 'inREPAIR' and not instance.owner:
            instance.status = 'AVAILABLE'
            instance.activityhistory_set.create(
                description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' +
                'Got back from repairing by ' + request.user.get_full_name())
            messages.info(request, instance.serial_number +
                          ' (' + instance.model_type.name + ') ' + "was Repaired.")

        instance.save()

    return redirect('supported-instance-list')


class InstanceOwnerUpdate(LoginRequiredMixin, UpdateView):
    model = Instance
    fields = ['owner']  # fields = '__all__'
    template_name = 'nanoassets/instance_update_owner.html'
    success_url = reverse_lazy('nanoassets:supported-instance-list')

    def form_valid(self, form):
        original_instance = Instance.objects.get(pk=form.instance.pk)
        if form.instance.owner:
            form.instance.status = 'inUSE'  # self.object.status = 'inUSE'
            self.object.activityhistory_set.create(
                description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' +
                'The IT Assets was Assigned to ' + form.instance.owner.username + ' from ' + (original_instance.owner.username if original_instance.owner else ' 🈳 ') + ' by ' + self.request.user.get_full_name())
            messages.info(self.request, 'The IT Assets was Assign to ' +
                          form.instance.owner.username + ' from ' + (original_instance.owner.username if original_instance.owner else ' 🈳 '))
        else:
            form.instance.status = 'AVAILABLE'  # self.object.status = 'AVAILABLE'
            self.object.activityhistory_set.create(
                description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' +
                'The IT Assets was Returned from ' + original_instance.owner.username + ' by ' + self.request.user.get_full_name())
            messages.info(self.request, 'The IT Assets was Returned from ' + original_instance.owner.username)

        return super().form_valid(form)


class InstanceByTechListView(LoginRequiredMixin, generic.ListView):
    model = Instance
    template_name = 'nanoassets/instance_list_by_tech.html'
    paginate_by = 15

    def get_queryset(self):
        return super().get_queryset().filter(branchSite__onSiteTech=self.request.user)  # 跨多表查询


class InstanceByUserListView(LoginRequiredMixin, generic.ListView):
    model = Instance
    template_name = 'nanoassets/instance_list_by_user.html'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user).filter(status__exact='inUSE').order_by('eol_date')
        # return Instance.objects.filter(owner=self.request.user).filter(status__exact='u').order_by('eol_date')

class InstanceDetailView(LoginRequiredMixin, generic.DetailView):
    model = Instance
    

class InstanceListView(LoginRequiredMixin, generic.ListView):
    model = Instance
    paginate_by = 15


def index(request):
    return render(request, "index.html", {})
