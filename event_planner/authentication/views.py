from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse

# Create your views here.

from .forms import SignUpForm


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Your account was successfully created.')
            return HttpResponseRedirect('/')
        elif not form.is_valid():
            messages.add_message(request, messages.WARNING,
                                 'There were problems creating your account, please review the information given and'
                                 ' try again')
            return render(request, 'authentication/signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'authentication/signup.html', {'form': form})
