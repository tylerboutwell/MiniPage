from django.shortcuts import render, redirect
from profiles.forms import ProfileForm
from django.contrib import messages

def create_profile(request):
    form = ProfileForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                create_profile = form.save(commit=False)
                create_profile.user = request.user
                create_profile.save()
                messages.success(request, "You have created your profile!")
                return redirect('core:home')
        return render(request, 'profiles/create_profile.html', {'form': form})
    else:
        messages.success(request, "You must be logged in to create profile.")
        return redirect('core:home')