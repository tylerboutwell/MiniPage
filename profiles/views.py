from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods


from profiles.forms import ProfileForm, LinkForm
from django.contrib import messages
from profiles.models import Profile, Link
from profiles.utils import reorder, get_max_position


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
            link.position = get_max_position(profile)
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
            link.profile = profile
            form.save()
            messages.success(request, "Your link has been updated!")
            return render(request, "profiles/partials/link_row.html", {"link": link, "profile": profile, "form": form})
        else:
            return render(request, "profiles/partials/edit_link_row.html", {
                "form": form,
                "link": link,
                "profile": profile,
            })
    return render(request, 'profiles/partials/edit_link_row.html', {
        'form': form,
        'profile': profile,
        'link': link
    })

@login_required
def link_row(request, profile_id, link_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    link = get_object_or_404(Link, id=link_id, profile=request.user.profile)
    return render(request, "profiles/partials/link_row.html", {"link": link, "profile": profile})

@require_http_methods(['DELETE'])
@login_required
def delete_link(request, profile_id, link_id):
    profile = get_object_or_404(Profile, pk=profile_id)
    link = get_object_or_404(Link, pk=link_id, profile=profile)
    if link.profile == request.user.profile:
        link.delete()
        reorder(profile)
        messages.success(request, "Your link has been deleted.")
        return HttpResponse("")
    else:
        messages.warning(request, "You are not allowed to delete this link.")
        return redirect('profiles:profile_detail', profile_id=profile_id)

@login_required
@require_http_methods(['POST'])
def reorder_links(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id, user=request.user)

    link_ids = request.POST.getlist("link_order")
    links = []

    for index, link_id in enumerate(link_ids, start=1):
        link = Link.objects.get(pk=link_id)
        link.position = index
        link.save()
        links.append(link)


    return render(request, 'profiles/partials/link_list.html', {"profile": profile, "links": links})

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.http import HttpResponse

def r2_test_upload(request):
    return HttpResponse(f"Current storage backend: {default_storage.__class__}")