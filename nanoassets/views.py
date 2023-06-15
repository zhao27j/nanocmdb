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
# from django.views.generic.edit import CreateView, UpdateView, DeleteView
# from django.urls import reverse_lazy
from django.utils import timezone

from django.db.models import Q

from .forms import NewInstanceForm, InstnaceOwnerUpdateForm, InstanceHostnameUpdateForm
from .models import ModelType, Instance, ScrapRequest, branchSite
from nanopay.models import Contract
from nanobase.models import ChangeHistory

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
                        # selected_instance.activityhistory_set.create(description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' + 'Transferred to ' + request.POST['branchsite_selected'] + ' from ' + selected_instance.branchSite.name + ' by ' + request.user.get_full_name())
                        
                        ChangeHistory.objects.create(
                            on=timezone.now(),
                            by=request.user,
                            db_table_name=selected_instance._meta.db_table,
                            db_table_pk=selected_instance.pk,
                            detail='Transferred to ' + request.POST['branchsite_selected'] + ' from ' + selected_instance.branchSite.name
                            )
                        
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
                        # contract_selected.activityhistory_set.create(description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' + 'Associated with the IT Assets [ ' + selected_instance.serial_number + ' ] by ' + request.user.get_full_name())
                        
                        ChangeHistory.objects.create(
                            on=timezone.now(),
                            by=request.user,
                            db_table_name=contract_selected._meta.db_table,
                            db_table_pk=contract_selected.pk,
                            detail='Associated with the IT Assets [ ' + selected_instance.serial_number + ' ]'
                            )
                        
                        contract_selected.save()

                        # selected_instance.activityhistory_set.create(description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' + 'Associated with the Contract [ ' + contract_selected.briefing + ' ] by ' + request.user.get_full_name())
                        
                        ChangeHistory.objects.create(
                            on=timezone.now(),
                            by=request.user,
                            db_table_name=selected_instance._meta.db_table,
                            db_table_pk=selected_instance.pk,
                            detail='Associated with the Contract [ ' + contract_selected.briefing + ' ]'
                            )
                        
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
                Q(model_type__sub_category__name__icontains=query) |
                Q(status__icontains=query) |
                Q(owner__username__icontains=query) |
                Q(owner__first_name__icontains=query) |
                Q(owner__last_name__icontains=query) |
                Q(owner__email__icontains=query) |
                Q(hostname__icontains=query) |
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
            # instance.activityhistory_set.create(description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' + 'Sent to repair by ' + request.user.get_full_name())
            
            ChangeHistory.objects.create(
                on=timezone.now(),
                by=request.user,
                db_table_name=instance._meta.db_table,
                db_table_pk=instance.pk,
                detail='Sent to repair'
                )
            
            messages.info(request, instance.serial_number + ' (' + instance.model_type.name + ') ' + "was sent to repair")
        elif instance.status == 'inREPAIR' and instance.owner:
            instance.status = 'inUSE'
            # instance.activityhistory_set.create(description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' + 'Got back from repairing by ' + request.user.get_full_name())
            
            ChangeHistory.objects.create(
                on=timezone.now(),
                by=request.user,
                db_table_name=instance._meta.db_table,
                db_table_pk=instance.pk,
                detail='Got back from repairing'
                )
            
            messages.info(request, instance.serial_number + ' (' + instance.model_type.name + ') ' + "was Repaired")
        elif instance.status == 'inREPAIR' and not instance.owner:
            instance.status = 'AVAILABLE'
            # instance.activityhistory_set.create(description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' + 'Got back from repairing by ' + request.user.get_full_name())
            
            ChangeHistory.objects.create(
                on=timezone.now(),
                by=request.user,
                db_table_name=instance._meta.db_table,
                db_table_pk=instance.pk,
                detail='Got back from repairing'
                )
            
            messages.info(request, instance.serial_number + ' (' + instance.model_type.name + ') ' + "was Repaired")

        instance.save()

    return redirect('nanoassets:supported-instance-list')


def InstanceHostnameUpdate(request, pk):
    instance = get_object_or_404(Instance, pk=pk)
    if request.method == 'POST':
        form = InstanceHostnameUpdateForm(request.POST)
        if form.is_valid():
            new_hostname = form.cleaned_data.get('hostname').strip()

            # instance.activityhistory_set.create(description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' + 'the Hostname of IT Assets [ ' + instance.serial_number + ' ] was updated from [ ' + instance.hostname + ' ] to [ ' + new_hostname + ' ] by ' + request.user.get_full_name())
            
            ChangeHistory.objects.create(
                on=timezone.now(),
                by=request.user,
                db_table_name=instance._meta.db_table,
                db_table_pk=instance.pk,
                detail='the Hostname of IT Assets [ ' + instance.serial_number + ' ] was updated from [ ' + instance.hostname + ' ] to [ ' + new_hostname + ' ]'
                )
            
            messages.info(request, 'the Hostname of IT Assets [ ' + instance.serial_number + 
                ' ] was updated from [ ' + instance.hostname + ' ] to [ ' + new_hostname + ' ]')

            instance.hostname = new_hostname

            instance.save()

            return redirect('nanoassets:instance-detail', pk=instance.pk)

    else: # if this is a GET (or any other method) create the default form.
        form = InstanceHostnameUpdateForm(initial={
            'hostname': 'TS-' + instance.serial_number,
        })

    return render(request, 'nanoassets/instance_update_hostname.html', {
        'form': form,
        'instance': instance,
        })



@login_required
def InstanceOwnerUpdate(request, pk):
    owner_list = []
    for owner in User.objects.all():
        if owner.username != 'admin' and 'tishmanspeyer.com' in owner.email:
            owner_list.append('%s ( %s )' % (owner.get_full_name(), owner.username))

    instance = get_object_or_404(Instance, pk=pk)

    if request.method == 'POST': # if this is a POST request then process the Form data
        form = InstnaceOwnerUpdateForm(request.POST) # create a form instance and populate it with data from the request (binding):
        if form.is_valid(): # check if the form is valid:
            # process the data in form.cleaned_data as required
            re_assign_to = form.cleaned_data.get('owner').strip(")").split("(")[-1].strip().lower()
            re_assign_to = get_object_or_404(User, username=re_assign_to) if re_assign_to != '' else re_assign_to
            if re_assign_to == '' and instance.owner:

                # instance.activityhistory_set.create(description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' + 'Returned from [ ' + instance.owner.get_full_name() + ' ] by ' + request.user.get_full_name())
                
                ChangeHistory.objects.create(
                    on=timezone.now(),
                    by=request.user,
                    db_table_name=instance._meta.db_table,
                    db_table_pk=instance.pk,
                    detail='Returned from [ ' + instance.owner.get_full_name() + ' ]'
                    )

                messages.info(request, 'the IT Assets [ ' + instance.serial_number + ' ] was Returned from ' + instance.owner.username)

                instance.status = 'AVAILABLE'
                instance.owner = None
                instance.save()

                return redirect('nanoassets:instance-detail', pk=instance.pk)
            
            elif re_assign_to != '' and re_assign_to != instance.owner:

                # instance.activityhistory_set.create(description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' + 'Re-assigned to [ ' + re_assign_to.get_full_name() + ' ] from [ ' + (instance.owner.get_full_name() if instance.owner else ' 🈳 ') + ' ] by ' + request.user.get_full_name())
                
                ChangeHistory.objects.create(
                    on=timezone.now(),
                    by=request.user,
                    db_table_name=instance._meta.db_table,
                    db_table_pk=instance.pk,
                    detail='Re-assigned to [ ' + re_assign_to.get_full_name() + ' ] from [ ' + (instance.owner.get_full_name() if instance.owner else ' 🈳 ') + ' ]'
                    )
                
                messages.info(request, 'the IT Assets [ ' + instance.serial_number + ' ] was Re-assigned to ' +
                                re_assign_to.get_full_name() + ' from ' + (instance.owner.get_full_name() if instance.owner else ' 🈳 '))

                instance.status = 'inUSE'
                instance.owner = re_assign_to
                instance.save()

                return redirect('nanoassets:instance-detail', pk=instance.pk)

            else:
                messages.warning(request, 'the ownership of IT Assets [ ' + instance.serial_number + ' ] got Nothing to change')

    else: # if this is a GET (or any other method) create the default form.
        form = InstnaceOwnerUpdateForm(initial={})

    return render(request, 'nanoassets/instance_update_owner.html', {
        'form': form,
        'owner_list': owner_list,
        'instance': instance,
        })


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        changes = ChangeHistory.objects.filter(db_table_name=self.object._meta.db_table, db_table_pk=self.object.pk).order_by("-on")
        context["changes"] = changes
        return context


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

            # new_instance.activityhistory_set.create(description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' + 'a New IT Assets was added by ' + request.user.get_full_name())
            
            ChangeHistory.objects.create(
                    on=timezone.now(),
                    by=request.user,
                    db_table_name=new_instance._meta.db_table,
                    db_table_pk=new_instance.pk,
                    detail='1 x New IT Assets was added'
                    )
            
            contract_associated_with = get_object_or_404(Contract, briefing=form.cleaned_data['contract'].strip())
            contract_associated_with.assets.add(new_instance)

            # contract_associated_with.activityhistory_set.create(description='[ ' + timezone.now().strftime("%Y-%m-%d %H:%M:%S") + ' ] ' + 'a New IT Assets [ ' + new_instance.serial_number + ' ] was associated with this Contract by ' + request.user.get_full_name())
            
            ChangeHistory.objects.create(
                    on=timezone.now(),
                    by=request.user,
                    db_table_name=contract_associated_with._meta.db_table,
                    db_table_pk=contract_associated_with.pk,
                    detail='1 x New IT Assets [ ' + new_instance.serial_number + ' ] was associated with this Contract'
                    )

            messages.info(request, 'the New IT Assets [ ' + form.cleaned_data['serial_number'] + ' ] was added')

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
