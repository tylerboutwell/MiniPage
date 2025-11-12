from django.shortcuts import render, get_object_or_404
from profiles.models import Profile
from django.contrib.auth.models import User

def home(request):
    if request.user.is_authenticated:
        profile_id = Profile.objects.get(user=request.user).id
        username = request.user.username
        return render(request, 'core/home.html', context={'profile_id': profile_id, 'username': username})
    return render(request, 'core/home.html')

def minipage_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    links = profile.links.all()
    return render(request, 'core/minipage.html', {'links': links, 'profile': profile})