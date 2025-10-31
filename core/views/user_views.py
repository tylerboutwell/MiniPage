from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect
from ..forms import SignUpForm

def home(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('core:home')
        else:
            messages.success(request, 'Invalid username or password')
            return redirect('core:home')
    else:
        return render(request, 'core/home.html')

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You Have Successfully Registered! Welcome!")
            return redirect('core:home')
    else:
        form = SignUpForm()
        return render(request, 'registration/register.html', {'form':form})
    return render(request, 'registration/register.html', {'form':form})