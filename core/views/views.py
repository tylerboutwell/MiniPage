from django.shortcuts import render, get_object_or_404
from profiles.models import Profile

def home(request):
    return render(request, 'core/home.html')

def minipage_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    links = profile.links.all()
    return render(request, 'core/minipage.html', {'links': links, profile: profile})