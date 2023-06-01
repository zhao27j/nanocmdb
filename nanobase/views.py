from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from .forms import UserProfileUpdateForm

# Create your views here.

@login_required
def user_profile_update(request):
    if request.method == 'POST': # if this is a POST request then process the Form data
        form = UserProfileUpdateForm(
            request.POST,
            # request.FILES,
            instance=request.user.userprofile)
        
        if form.is_valid():
            form.save()
            return redirect(to='')
    else:
        form = UserProfileUpdateForm()

    return render(request, 'nanobase/user_profile.html', {'form': form})