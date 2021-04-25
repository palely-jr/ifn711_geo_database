from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Accounts


def home(request):
    return render(request, 'index/home.html')


def signin(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST["password"]
        user_account = authenticate(username=username, password=password)
        if user_account:
            if user_account.is_active:
                login(request, user_account)
                return redirect('')
            # throw error
            else:
                return render(request, 'signin/signin.html', {
                    'login_disabled': 'account disabled'
                })
        else:
            return render(request, 'signin/signin.html', {
                'invalid': 'Please Input Valid Login'
            })

    else:
        return render(request, 'signin/signin.html', {})


# register user form
def register(request):
    print("this is touched")
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        # data cleaning
        name = request.POST['name']
        email = request.POST['email']
        dob = request.POST['dob']
        password = request.POST['passwordOne']
        user = User.objects.create_user(name, email, password)
        user.save()
        return render(request, 'registration/registration.html', {})
    else:
        return render(request, 'registration/registration.html', {})
