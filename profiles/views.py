from django.shortcuts import render

def create_profile(request):
    return render(request, 'profiles/create_profile.html')