from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from event_planner.authentication.forms import SignUpForm
from event_planner.authentication.tokens import account_activation_token
from event_planner.authentication.models import Profile

# Create your views here.


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your SwiftPlanner Account'
            message = render_to_string('authentication/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return render(request, "authentication/activation_sent.html", {'email': user.email})
        elif not form.is_valid():
            messages.add_message(request, messages.ERROR,
                                 'There were problems creating your account, please review the information given and'
                                 ' try again')
            return render(request, 'authentication/signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'authentication/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_verified = True
        user.profile.save()
        user.save()
        login(request, user)
        return redirect('core:home')
    else:
        return render(request, 'authentication/account_activation_invalid.html')
