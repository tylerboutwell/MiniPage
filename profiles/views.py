from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from profiles.forms import ProfileForm, LinkForm
from django.contrib import messages
from profiles.models import Profile, Link


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

@login_required
def profile_detail(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    links = profile.links.all()
    if profile.user == request.user:
        return render(request, 'profiles/profile_detail.html',
                      {'profile': profile, 'links': links})
    else:
        messages.warning(request, "You are not allowed to see this page.")
        return redirect('core:home')

@login_required
def edit_profile(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    if profile.user == request.user:
        form = ProfileForm(request.POST or None, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profiles:profile_detail', profile_id=profile_id)
        else:
            return render(request, 'profiles/edit_profile.html',
                          {"form": form, 'profile': profile})
@login_required
def add_link(request, profile_id):
    form = LinkForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            link = form.save(commit=False)
            link.profile = request.user.profile
            form.save()
            messages.success(request, "Your link has been added!")
            return redirect('profiles:profile_detail', profile_id)
        else:
            messages.warning(request, "Invalid link.")
            return redirect('core:home')
    else:
        return render(request, 'profiles/add_link.html',
                      {'form': form, 'profile_id': profile_id})

@login_required
def edit_link(request, profile_id, link_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    link = get_object_or_404(Link, pk=link_id, profile=profile)
    form = LinkForm(request.POST or None, instance=link)
    if request.method == 'POST':
        if form.is_valid():
            link = form.save(commit=False)
            link.profile = request.user.profile
            form.save()
            messages.success(request, "Your link has been updated!")
            return redirect('profiles:profile_detail', profile_id=profile_id)
        else:
            messages.warning(request, "Invalid link.")
            return redirect('profiles:profile_detail', profile_id=profile_id)
    else:
        return render(request, 'profiles/edit_link.html',
                      {'form': form, 'profile': profile, 'link': link})