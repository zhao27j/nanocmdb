from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.views.generic.edit import CreateView

from nanoassets.models import Instance

from .forms import UserProfileUpdateForm

# Create your views here.

class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email', ] # '__all__'
    # template_name = "TEMPLATE_NAME"
    success_url = reverse_lazy('nanoassets:supported-instance-list')


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

"""
def data_migration_Hostname(request):
    instances = Instance.objects.all()
    for instance in instances:
        if instance.configuragion:
            instance.hostname = instance.configuragion.hostname
            instance.save()

    return redirect(request.path) # 重定向 至 当前 页面
"""