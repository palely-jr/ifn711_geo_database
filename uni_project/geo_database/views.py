from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Accounts


#basic homepage --> needs to be done
def home(request):
    return render(request, 'index/home.html')


def signin(request):
    #use this to authenticate each request made
    if request.user.is_authenticated:
        return redirect('/')
    #this to post
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST["password"]
        #we use this to authenticat the user
        user_account = authenticate(username=username, password=password)
        #check if user is authenticated
        if user_account:
            if user_account.is_active:
                login(request, user_account)
                return HttpResponseRedirect(reverse('geo-home'))
            # throw error
            else:
                return render(request, 'signin/signin.html', {
                    'login_disabled': 'account disabled'
                })
        #pass through different error messages for error validation on client side
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
        #assignment
        username = request.POST['username']
        name = request.POST['name']
        email = request.POST['email']
        dob = request.POST['dob']
        #end assignment
        password = request.POST['passwordOne']
        #you dont need to put each POST form element into a variable
        #i just found it more readable
        #store them as a user, in mysql auth_user is the best user table for us
        user = User.objects.create_user(username=username, first_name=name, email=email, password=password, )
        #save it to db
        user.save()
        #redirect back to signin page, check geo_database.urls to see the names (im using a geo-xxx ..
        # naming convention)
        return HttpResponseRedirect(reverse('geo-signin'))
    else:

        return render(request, 'registration/registration.html', {})


#signs out user, pre simple
def signout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('geo-signin'))
