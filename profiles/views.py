from django.shortcuts import render, redirect, get_object_or_404
from profiles.forms import ProfileForm
from django.contrib import messages
from profiles.models import Profile

def create_profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in to create profile.")
        return redirect('core:home')

    if Profile.objects.filter(user=request.user).exists():
        messages.info(request, "You already have a profile.")
        return redirect('core:home')

    form = ProfileForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, "You have created your profile!")
            return redirect('core:home')
    return render(request, 'profiles/create_profile.html', {'form': form})

def profile_detail(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    if profile.user == request.user:
        return render(request, 'profiles/profile_detail.html', {'profile': profile})
    else:
        messages.warning(request, "You are not allowed to see this page.")
        return redirect('core:home')