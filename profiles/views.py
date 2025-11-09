from django.shortcuts import render, redirect
from profiles.forms import ProfileForm
from django.contrib import messages

def create_profile(request):
    if not request.user.is_authenticated:
        messages.warning(request, "You must be logged in to create profile.")
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