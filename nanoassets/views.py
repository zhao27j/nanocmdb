from django.shortcuts import render, get_object_or_404, redirect

# from django.http import HttpResponse, HttpResponseRedirect

from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
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

from .forms import NewInstanceForm
from .models import ModelType, Instance, ScrapRequest, branchSite
from nanopay.models import Contract

# Create your views here.

@login_required
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

        IT_reviewer_emails = []
        for reviewer in User.objects.filter(groups__name='IT Reviewer'):
            IT_reviewer_emails.append(reviewer.email)

        message = get_template("nanoassets/instance_scrapping_request_approved_email.html").render({
            'protocol': 'http',
            'domain': '127.0.0.1:8000',
            # 'instances': request.POST.getlist('instance'),
            'scrapRequest': scrapRequest,
        })
        mail = EmailMessage(
            subject='ITS express - Please notice - Scrapping Request is approved by ' +
            scrapRequest.approved_by.get_full_name(),
            body=message,
            from_email='nanoMessenger <do-not-reply@tishmanspeyer.com>',
            to=[scrapRequest.requested_by.email],
            cc=IT_reviewer_emails,
            # reply_to=[EMAIL_ADMIN],
            # connection=
        )
        mail.content_subtype = "html"
        mail.send()
        messages.success(
            request, "the notification email with the apprival decision is sent.")

        return redirect('nanoassets:instance-scrapping-request-list')


class InstanceScrappingRequestDetailView(LoginRequiredMixin, generic.DetailView):
    model = ScrapRequest
    template_name = 'nanoassets/instance_scrapping_request_detail.html'


class InstanceScrappingRequestListView(LoginRequiredMixin, generic.ListView):
    model = ScrapRequest
    template_name = 'nanoassets/instance_scrapping_request_list.html'
    # paginate_by = 10


@login_required
def InstanceBulkUpd(request):
    if request.method == 'POST':
        if request.POST.getlist('instance'):
            if 'scrapping-request' in request.POST or 'branchsite-transfer' in request.POST:
                for selected_instance_pk in request.POST.getlist('instance'):
                    selected_instance = get_object_or_404(Instance, pk=selected_instance_pk)
                    if selected_instance.status != 'AVAILABLE' or selected_instance.scrap_request:
                        messages.warning(request, "only unrequested Available computers can be requested")
                        # return redirect(request.path) # 重定向 至 当前 页面 (在此不适合)
                        return redirect(request.META.get('HTTP_REFERER')) # 重定向 至 前一个 页面

            if 'scrapping-request' in request.POST:
                new_scrap_request = ScrapRequest.objects.create(requested_by=request.user)
                new_scrap_request.save()

                for selected_instance_pk in request.POST.getlist('instance'):
                    selected_instance = get_object_or_404(Instance, pk=selected_instance_pk)
                    selected_instance.scrap_request = new_scrap_request
                    selected_instance.save()

                IT_reviewer_emails = []
                for reviewer in User.objects.filter(groups__name='IT Reviewer'):
                    IT_reviewer_emails.append(reviewer.email)

                message = get_template("nanoassets/instance_scrapping_request_email.html").render({
                    'protocol': 'http',
                    'domain': '127.0.0.1:8000',
                    'new_scrap_request': new_scrap_request,
                })
                mail = EmailMessage(
                    subject='ITS express - Please approve - scrapping IT assets requested by ' + new_scrap_request.requested_by.get_full_name(),
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

                return redirect('nanoassets:instance-scrapping-request-list')

            elif 'branchsite-transfer' in request.POST:
                try:
                    branchsite_selected = branchSite.objects.get(name=request.POST['branchsite_selected'])
                except (KeyError, branchSite.DoesNotExist):
                    messages.info(request, 'distination Site given is invalid')
                else:
                    for selected_instance_pk in request.POST.getlist('instance'):
                        selected_instance = get_object_or_404(Instance, pk=selected_instance_pk)
                        selected_instance.activityhistory_set.create(
                            description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' +
                            'Transferred to ' + request.POST['branchsite_selected'] + ' from ' + selected_instance.branchSite.name + ' by ' + request.user.get_full_name())
                        selected_instance.branchSite = get_object_or_404(branchSite, name=request.POST['branchsite_selected'])
                        selected_instance.save()
                    messages.info(request, 'the selected IT Assets were Transferred to ' + request.POST['branchsite_selected'])

                # return redirect('nanoassets:supported-instance-list')
            elif 'contract-associate' in request.POST:
                try:
                    contract_selected = Contract.objects.get(briefing=request.POST['contract_selected'])
                except (KeyError, Contract.DoesNotExist):
                    messages.info(request, 'Contract given is invalid')
                else:
                    for selected_instance_pk in request.POST.getlist('instance'):
                        selected_instance = get_object_or_404(Instance, pk=selected_instance_pk)
                        contract_selected.assets.add(selected_instance)
                        contract_selected.activityhistory_set.create(
                            description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' +
                            'Associated with the IT Assets [ ' + selected_instance.serial_number + ' ] by ' + request.user.get_full_name())
                        contract_selected.save()
                        selected_instance.activityhistory_set.create(
                            description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' +
                            'Associated with the Contract [ ' + contract_selected.briefing + ' ] by ' + request.user.get_full_name())
                        selected_instance.save()
                    messages.info(request, 'the selected IT Assets were Associated with the Contract [ ' + request.POST['contract_selected'] + ' ]')
                    
            return redirect(request.META.get('HTTP_REFERER')) # 重定向 至 前一个 页面
        else:
            messages.info(request, "no IT Assets were selected")
            # return redirect('nanoassets:supported-instance-list')
            return redirect(request.META.get('HTTP_REFERER')) # 重定向 至 前一个 页面


class InstanceSearchResultsListView(LoginRequiredMixin, generic.ListView):
    model = Instance
    template_name = 'nanoassets/instance_list_search_results.html'
    paginate_by = 32

    def get_queryset(self):
        queries = tuple(self.request.GET.get('q').split(','))
        object_list = Instance.objects.filter(
            branchSite__onSiteTech=self.request.user)

        for query in queries:
            query = query.strip()
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

        if object_list:
            messages.info(self.request, "%s results found" %
                          object_list.count())
        else:
            messages.info(self.request, "no results found")
            # self.request.GET = self.request.GET.copy()
            # self.request.GET['q'] = ''

        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        branchSites_name = []
        for site in branchSite.objects.all():
            branchSites_name.append(site)
        context["branchSites_name"] = branchSites_name

        contracts = []
        for contract in Contract.objects.all():
            contracts.append(contract)
        context['contracts'] = contracts

        return context


@login_required
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
                          instance.model_type.name + ') ' + "was sent to repair")
        elif instance.status == 'inREPAIR' and instance.owner:
            instance.status = 'inUSE'
            instance.activityhistory_set.create(
                description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' +
                'Got back from repairing by ' + request.user.get_full_name())
            messages.info(request, instance.serial_number +
                          ' (' + instance.model_type.name + ') ' + "was Repaired")
        elif instance.status == 'inREPAIR' and not instance.owner:
            instance.status = 'AVAILABLE'
            instance.activityhistory_set.create(
                description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' +
                'Got back from repairing by ' + request.user.get_full_name())
            messages.info(request, instance.serial_number +
                          ' (' + instance.model_type.name + ') ' + "was Repaired")

        instance.save()

    return redirect('nanoassets:supported-instance-list')


class InstanceOwnerUpdate(LoginRequiredMixin, UpdateView):
    model = Instance
    fields = ['owner']  # fields = '__all__'
    template_name = 'nanoassets/instance_update_owner.html'
    success_url = reverse_lazy('nanoassets:supported-instance-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        owners = []
        for owner in User.objects.all():
            if owner.username != 'admin':
                owners.append(owner)
        context['owners'] = owners
        return context

    def form_valid(self, form):
        original_instance = get_object_or_404(Instance, pk=form.instance.pk)
        assign_to = self.request.POST['assign_to'].strip()
        if assign_to == 'admin':
            form.instance.owner = original_instance.owner
            messages.warning(self.request, 'the IT Assets [ ' + original_instance.serial_number + ' ] can NOT be assigned to ' + assign_to)
        elif assign_to == '' and original_instance.owner == None:
            form.instance.owner = original_instance.owner
            messages.warning(self.request, 'the ownership of IT Assets [ ' + original_instance.serial_number + ' ] got Nothing to change')
        elif assign_to == '' and original_instance.owner:
            form.instance.status = 'AVAILABLE'  # self.object.status = 'AVAILABLE'
            self.object.activityhistory_set.create(
                description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' +
                'Returned from ' + original_instance.owner.username + ' by ' + self.request.user.get_full_name())
            messages.info(self.request, 'the IT Assets [ ' + original_instance.serial_number +
                          ' ] was Returned from ' + original_instance.owner.username)
        else:
            try:
                form.instance.owner = User.objects.get(username=assign_to)
            except User.DoesNotExist:
                form.instance.owner = None

            if not original_instance.owner:
                if not form.instance.owner:
                    form.instance.owner = original_instance.owner
                    messages.warning(self.request, 'the IT Assets [ ' + original_instance.serial_number + ' ] can NOT be assigned to ' + assign_to)
                elif assign_to == "":
                    form.instance.owner = original_instance.owner
                    messages.warning(self.request, 'the ownership of IT Assets [ ' + original_instance.serial_number + ' ] got Nothing to change')
                else:
                    form.instance.status = 'inUSE'  # self.object.status = 'inUSE'
                    self.object.activityhistory_set.create(
                        description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' + 'Assigned to ' + form.instance.owner.username + ' from ' + (original_instance.owner.username if original_instance.owner else ' 🈳 ') + ' by ' + self.request.user.get_full_name())
                    messages.info(self.request, 'the IT Assets [' + original_instance.serial_number + '] was Assign to ' +
                                form.instance.owner.username + ' from ' + (original_instance.owner.username if original_instance.owner else ' 🈳 '))
            else:
                if not form.instance.owner:
                    form.instance.owner = original_instance.owner
                    messages.warning(
                        self.request, 'the IT Assets [ ' + original_instance.serial_number + ' ] can NOT be assigned to ' + assign_to)
                elif assign_to == original_instance.owner.username:
                    form.instance.owner = original_instance.owner
                    messages.warning(
                        self.request, 'the ownership of IT Assets [ ' + original_instance.serial_number + ' ] got Nothing to change')
                else:
                    form.instance.status = 'inUSE'  # self.object.status = 'inUSE'
                    self.object.activityhistory_set.create(
                        description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' + 'Assigned to ' + form.instance.owner.username + ' from ' + (original_instance.owner.username if original_instance.owner else ' 🈳 ') + ' by ' + self.request.user.get_full_name())
                    messages.info(self.request, 'the IT Assets [' + original_instance.serial_number + '] was Assign to ' +
                                form.instance.owner.username + ' from ' + (original_instance.owner.username if original_instance.owner else ' 🈳 '))

        return super().form_valid(form)


class InstanceByTechListView(LoginRequiredMixin, generic.ListView):
    model = Instance
    template_name = 'nanoassets/instance_list_by_tech.html'
    paginate_by = 32

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        branchSites_name = []
        for site in branchSite.objects.all():
            branchSites_name.append(site)
        context["branchSites_name"] = branchSites_name

        contracts = []
        for contract in Contract.objects.all():
            contracts.append(contract)
        context['contracts'] = contracts

        return context

    def get_queryset(self):
        return super().get_queryset().filter(branchSite__onSiteTech=self.request.user)  # 跨多表查询


class InstanceByUserListView(LoginRequiredMixin, generic.ListView):
    model = Instance
    template_name = 'nanoassets/instance_list_by_user.html'

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user).filter(status__icontains='use').order_by('eol_date')
        # return Instance.objects.filter(owner=self.request.user).filter(status__exact='u').order_by('eol_date')


class InstanceDetailView(LoginRequiredMixin, generic.DetailView):
    model = Instance


@login_required
def InstanceNew(request):
    model_type_list = []
    for model_type in ModelType.objects.all():
        model_type_list.append('%s ( %s )' % (model_type.name, model_type.manufacturer))

    owner_list = []
    for owner in User.objects.all():
        if owner.username != 'admin' and 'tishmanspeyer.com' in owner.email:
            owner_list.append('%s ( %s )' % (owner.get_full_name(), owner.username))
        
    branchsite_list = branchSite.objects.all()

    contract_list = Contract.objects.all()
    
    if request.method == 'POST':
        form = NewInstanceForm(request.POST)
        if form.is_valid():
            new_instance = Instance()
            new_instance.serial_number = form.cleaned_data['serial_number'].strip()
            new_instance.model_type = get_object_or_404(ModelType, name=form.cleaned_data['model_type'].split("(")[0].strip())
            new_instance.owner = get_object_or_404(User, username=form.cleaned_data['owner'].strip(")").split("(")[-1].strip())
            new_instance.status = form.cleaned_data['status'].strip()
            new_instance.branchSite = get_object_or_404(branchSite, name=form.cleaned_data['branchSite'].strip())

            new_instance.save()

            new_instance.activityhistory_set.create(
                description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' + 'a New IT Assets was added by ' + request.user.get_full_name()
                )
            
            contract_associated_with = get_object_or_404(Contract, briefing=form.cleaned_data['contract'].strip())
            contract_associated_with.assets.add(new_instance)

            contract_associated_with.activityhistory_set.create(
                description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' + 
                'a New IT Assets [ ' + new_instance.serial_number + ' ] was associated with this Contract by ' + request.user.get_full_name()
                )


            messages.info(request, 'the New IT Assets [ ' + form.cleaned_data['serial_number'] + ' ] was added by ' + request.user.get_full_name())

            return redirect('nanoassets:instance-detail', pk=new_instance.pk) # redirect to a new URL:
    else:
        form = NewInstanceForm()
    
    return render(request, 'nanoassets/instance_new.html', {
        'form': form,
        'model_type_list': model_type_list,
        'owner_list': owner_list,
        'branchsite_list': branchsite_list,
        'contract_list': contract_list
        })


@login_required
def index(request):
    return render(request, "index.html", {})
