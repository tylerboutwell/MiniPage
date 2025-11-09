from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.transaction import commit
from django.shortcuts import render, redirect
from ..forms import SignUpForm
from profiles.models import Profile

RESERVED_USERNAMES = {"login", "register", "admin", "about", "contact", "logout", "profile"}
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            username = form.cleaned_data['username'].lower()
            #Check if username isn't a reserved URL
            if username in RESERVED_USERNAMES:
                form.add_error("username", "This username is not allowed.")
                return render(request, "registration/register.html", {"form": form})

            password = form.cleaned_data['password1']
            form.save()
            user = authenticate(username=username, password=password)
            # Create a profile instance when a user is registered
            if user is not None:
                Profile.objects.create(user=user, profile_name = username)
                login(request, user)
                messages.success(request, "You Have Successfully Registered! Let's create your profile!")
                return redirect('profiles:create_profile')
            else:
                messages.error(request, "Authentication failed. Please try logging in.")
        else:
            messages.error(request, "There was a problem with your registration.")
    else:
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form':form})