import json
from functools import wraps
from django.contrib import messages
from django.urls import reverse
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm


# this decorator is for authenticating each request to the API
def authenticate_user(function):
    @wraps(function)
    def decorator(request, *args, **kwargs):

        payload = dict()
        incoming = json.loads(request.body)

        if not incoming['username'] or not incoming['password']:
            payload['status'] = 'bad'
            payload['data'] = dict()
            payload['data']['msg'] = 'invalid username or password'
            return JsonResponse(payload)

        user = authenticate(
            username=incoming['username'], password=incoming['password'])

        if user is None:
            payload['status'] = 'bad'
            payload['data'] = dict()
            payload['data']['msg'] = 'invalid username or password'
            return JsonResponse(payload)

        return function(request, user, *args, **kwargs)

    return decorator


def account_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if request.POST["next"] is not "":
                        return HttpResponseRedirect(request.POST["next"])
                    else:
                        return HttpResponseRedirect(reverse('overview_show'))
            else:
                text = "It seems you entered a wrong email or password. Please double check your credentials and try again."
                messages.add_message(request, messages.ERROR, text)
                return HttpResponseRedirect(reverse('account_login'))

        else:
            payload = {
                'form': form
            }
            return render(request, 'core/login.html', payload)
    else:

        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('dashboard:dashboard'))
        else:
            payload = {}

            if 'next' in request.GET:
                payload = {
                    'next': request.GET['next']
                }

            return render(request, 'core/login.html', payload)


def account_logout(request):
    logout(request)
    return render(request, 'core/login.html')
