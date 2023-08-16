from django.http import JsonResponse

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from nanoassets.models import Instance


@login_required
def jsonResponse_owner_lst(request):

    if request.method == 'GET':
        chk_lst = {}
        selected_instances_pk = tuple(request.GET.get('instanceSelectedPk').split(','))
        for index, pk in enumerate(selected_instances_pk):
            selected_instance = Instance.objects.get(pk=pk)
            # for branchSite in selected_instance.branchSite_set.all():
            owner = selected_instance.owner
            chk_lst[owner.username] = owner.pk

        owners = User.objects.filter(email__icontains='tishmanspeyer')
        opt_lst = {}
        for owner in owners:
            if not owner.username in chk_lst:
                opt_lst['%s ( %s )' % (owner.get_full_name(), owner.username)] = owner.pk
                # opt_lst[owner.get_full_name()] = owner.pk

        response = [opt_lst, chk_lst]
        return JsonResponse(response, safe=False)