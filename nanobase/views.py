# from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.http import Http404, FileResponse

from django.views.generic.edit import CreateView

from .models import UserDept, ChangeHistory, UploadedFile
from nanopay.models import LegalEntity
# from nanoassets.models import ActivityHistory

from .forms import UserProfileUpdateForm, UserCreateForm

# Create your views here.

class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', ] # '__all__'
    # template_name = "TEMPLATE_NAME"
    success_url = reverse_lazy('nanoassets:supported-instance-list')

@login_required
def user_create(request):
    dept_list = []
    for dept in UserDept.objects.all():
        dept_list.append(dept)

    legal_entity_list = []
    for legal_entity in LegalEntity.objects.all():
        legal_entity_list.append(legal_entity)

    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(
                username=form.cleaned_data.get('username').strip(),
                first_name=form.cleaned_data.get('first_name').strip(),
                last_name=form.cleaned_data.get('last_name').strip(),
                email=form.cleaned_data.get('email').strip(),
                )
            # new_user.save()

            new_user.userprofile.title = form.cleaned_data.get('title').strip() if form.cleaned_data.get('title') else ''
            new_user.userprofile.dept = UserDept.objects.get(name=form.cleaned_data.get('dept').strip()) if form.cleaned_data.get('dept') else None
            new_user.userprofile.work_phone = form.cleaned_data.get('work_phone')
            new_user.userprofile.cellphone = form.cleaned_data.get('cellphone')
            new_user.userprofile.postal_addr = form.cleaned_data.get('postal_addr').strip() if form.cleaned_data.get('postal_addr') else ''
            new_user.userprofile.legal_entity = LegalEntity.objects.get(name=form.cleaned_data.get('legal_entity').strip()) if form.cleaned_data.get('legal_entity') else None
            new_user.userprofile.save()

            if new_user.userprofile.legal_entity:
                ChangeHistory.objects.create(
                    on=timezone.now(),
                    by=request.user,
                    db_table_name=new_user.userprofile.legal_entity._meta.db_table,
                    db_table_pk=new_user.userprofile.legal_entity.pk,
                    detail='1 x Contact [ ' + new_user.get_full_name() + ' ] is created and associated with this Legal Entity'
                    )
                messages.info(request, '1 x Contact [ ' + new_user.get_full_name() + 
                              ' ] is created and associated with the Legal Entity [ ' + form.cleaned_data.get('legal_entity') + ' ]')
                return redirect(to='nanopay:legal-entity-list')
            else:
                messages.info(request, '1 x User [ ' + new_user.get_full_name() + ' ] is created')
                return redirect(to='/')
    else:
        form = UserCreateForm(initial={})

    return render(request, 'nanobase/user_create.html', {
        'form': form,
        'dept_list': dept_list,
        'legal_entity_list': legal_entity_list,
        })


@login_required
def user_profile_update(request, pk):
    if request.method == 'POST': # if this is a POST request then process the Form data
        form = UserProfileUpdateForm(
            request.POST,
            # request.FILES,
            instance=request.user.userprofile)
        
        if form.is_valid():
            form.save()
            return redirect(to='/')
    else:
        form = UserProfileUpdateForm(
            initial={
                # 'dept': request.user.userprofile.dept,
                # 'title': request.user.userprofile.title,
                'work_phone': request.user.userprofile.work_phone,
                'postal_addr': request.user.userprofile.postal_addr,
                'cellphone': request.user.userprofile.cellphone,
                # 'legal_entity': request.user.userprofile.legal_entity,
            }
        )

    return render(request, 'nanobase/user_profile_update.html', {'form': form})


@login_required
def get_digital_copy_display(request, pk):
    digital_copy_instance = get_object_or_404(UploadedFile, pk=pk)
    digital_copy_path = digital_copy_instance.digital_copy.name
    try:
        digital_copy = open(digital_copy_path, 'rb')
        # return FileResponse(digital_copy, content_type='application/pdf')
        return FileResponse(digital_copy)
    except FileNotFoundError:
        raise Http404


"""
def data_migration_ActivityHistory_to_ChangeHistory(request):
    activity_history_all = ActivityHistory.objects.all()
    for activity_history in activity_history_all:
        if activity_history.Instance:
            db_table_name = activity_history.Instance._meta.db_table
            db_table_pk = activity_history.Instance.pk
        elif activity_history.Contract:
            db_table_name = activity_history.Contract._meta.db_table
            db_table_pk = activity_history.Contract.pk

        on = activity_history.description.strip("[").split("]")[0].strip()
        detail = activity_history.description.split(on)[1].strip().strip("]").strip()
        ChangeHistory.objects.create(
                # by=request.user,
                on=datetime.strptime(on, "%Y-%m-%d %H:%M:%S"),
                db_table_name=db_table_name,
                db_table_pk=db_table_pk,
                detail=detail,
                )
            
    return redirect(request.META.get('HTTP_REFERER')) # 重定向 至 前一个 页面
"""