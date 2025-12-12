from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
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

    if profile.user != request.user:
        messages.error(request, "You are not allowed to edit this profile.")
        return redirect('core:home')

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profiles:profile_detail', profile_id=profile_id)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profiles/edit_profile.html',
                  {"form": form, 'profile': profile})
@login_required
def add_link(request, profile_id):
    profile = get_object_or_404(Profile, pk=profile_id, user=request.user)
    if request.method == 'POST':
        form = LinkForm(request.POST)
        if form.is_valid():
            link = form.save(commit=False)
            link.profile = request.user.profile
            form.save()
            messages.success(request, "Your link has been added!")
            return redirect('profiles:profile_detail', profile_id)
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = LinkForm()
    return render(request, 'profiles/add_link.html', {
        'form': form,
        'profile': profile
    })

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
            return render(request, "profiles/partials/link_row.html", {"link": link})
        else:
            return render(request, "profiles/partials/edit_link_row.html", {
                "form": form,
                "link": link,
                "profile": profile,
            })
    else:
        form = LinkForm(instance=link)
    return render(request, 'profiles/partials/edit_link_row.html', {
        'form': form,
        'profile': profile,
        'link': link
    })

@login_required
def link_row(request, link_id):
    link = get_object_or_404(Link, id=link_id, profile=request.user.profile)
    return render(request, "profiles/partials/link_row.html", {"link": link})

@login_required
def delete_link(request, profile_id, link_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    link = get_object_or_404(Link, pk=link_id, profile=profile)
    if link.profile == request.user.profile:
        link.delete()
        messages.success(request, "Your link has been deleted.")
        return HttpResponse("")
    else:
        messages.warning(request, "You are not allowed to delete this link.")
        return redirect('profiles:profile_detail', profile_id=profile_id)