from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from ..forms import SignUpForm
from profiles.models import Profile

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            # Create a profile instance when a user is registered
            Profile.objects.create(user=user, profile_name = username)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect('core:home')
    else:
        form = SignUpForm()
        return render(request, 'registration/register.html', {'form':form})
    return render(request, 'registration/register.html', {'form':form})