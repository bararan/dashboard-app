from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Profile
from .forms import ProfileForm

# Create your views here.

@login_required
def own_profile_view(req):
    profile = Profile.objects.get(user=req.user)
    form = ProfileForm(
        req.POST or None,
        req.FILES or None,
        instance=profile
    )
    confirmed = form.is_valid() #False
    print(req.POST)
    if confirmed:
        form.save()
        # confirmed = True
    context = {
        'profile': profile,
        'form': form,
        'confirmed': confirmed,
    }
    return render(req, 'profiles/main.html', context)