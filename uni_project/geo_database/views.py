from django.http.response import FileResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Items,fileStorage,Company
from django.core.mail import EmailMessage
from django.urls import reverse



#basic homepage --> needs to be done
def home(request):

    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        if request.method == 'GET':
            search = request.GET.get('search_term', False)
            if search:
                user_items = Items.objects.filter(user_id=user.pk, item_file__icontains=search)
                return render(request, 'index/home.html', {'user_items': user_items})
        #need to get all items with user.id and then put in context and put into the frontend
    return render(request, 'index/home.html')


def search(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            return render(request, 'index/home.html')
        return HttpResponseRedirect(reverse('geo-home'))
    return HttpResponseRedirect(reverse('geo-signin'))

def signin(request):
    #use this to authenticate each request made
    if request.user.is_authenticated:
        return redirect('geo-dashboard')
    #this to post
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST["password"]
        #we use this to authenticat the user
        user_account = authenticate(username=username, password=password)
        print("this is something", user_account)
        #check if user is authenticated
        if user_account:
            if user_account.is_active:
                 login(request, user_account)
                 return HttpResponseRedirect(reverse('geo-dashboard'))
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

def deleteItem(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            item_list = request.POST.getlist('delete_files')
            check_length = len(item_list)
            if check_length > 0:
                #do a for loop and delete each
                for item in item_list:
                    print("this is item: ", item)
                    Items.objects.filter(item_id=item).delete()
                return HttpResponseRedirect(reverse('geo-home'))
        return HttpResponseRedirect(reverse('geo-home'))
    return HttpResponseRedirect(reverse('geo-signin'))

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
        checkCompany= Company.objects.all();
        if checkCompany:
           print("Defualt Company Created")       
        else:
         company=Company.objects.create_Company(company_name="Default",company_email="default@gmail.com",company_type="Row Data")
         company.save()
        #save it to db
        
        #store them as a user, in mysql auth_user is the best user table for us
        user = User.objects.create_user(username=username, first_name=name, email=email, password=password,last_name="1" )
       #creating a file storage for new user
       
        user.is_active = True
        user.save()
        #redirect back to signin page, check geo_database.urls to see the names (im using a geo-xxx ..
        # naming convention)
        return HttpResponseRedirect(reverse('geo-signin'))
    else:

        return render(request, 'registration/registration.html', {})


def dashboard(request):
    print("this is touched")
    if request.user.is_authenticated:
     if request.user.is_superuser:
      username = request.user.username
      user = User.objects.get(username=username)
      return render(request, 'dashboard/admin/index.html',{'user_items': username})
     else:
      username = request.user.username
      user = User.objects.get(username=username)
      print(user.pk)
      #pulling file details
      fileDetails=fileStorage.objects.get(user=user.last_name)
      print(fileDetails.total_file_size);
     return render(request, 'dashboard/index.html',{'user_name': user.first_name,'total_file_size': fileDetails.total_file_size,'used_file_size': fileDetails.used_file_size,'remaining_file_size': fileDetails.remaining_file_size})
    else:
       return render(request,'signin/signin.html')

def filestoragealoc(request):
    if request.user.is_authenticated:
        #pulling file details
        fileDetails=fileStorage.objects.all()
        usersid=[]
        for userId in fileDetails:
             usersid.append(userId.company_id)
             #print("this is",usersid)
        
        print("this is",usersid)
        if request.method == 'POST':
         username = request.POST['userid']
         size = request.POST['size']
         print(username)
         userId_exists = usersid.count((username))  
         print(userId_exists)
         if userId_exists > 0:
          print("came here")
          fileDetail = fileStorage.objects.get(company_id=username)
          if fileDetail:
            print("came here again")
            fileDetail.total_file_size = size
            fileDetail.save()
            return HttpResponseRedirect(reverse('geo-filestoragealoc'))
             # throw error
          else:
            return render(request, 'signin/signin.html', {
                          'invalid': 'Please Input Valid Login'
              })
        return render(request, 'filestorage/index.html',{'filedetails': fileDetails})
    else:
       return render(request,'signin/signin.html')

def uploadItem(request):
    print("this is accessed")
    if request.user.is_authenticated:
        if request.method == 'POST':
            uploaded_file = request.FILES['file']
            file_name = request.POST['filename']
            username = request.user.username
            user = User.objects.get(username=username)
            new_item = Items.objects.create_item(uploaded_file, file_name, user.pk)
            return HttpResponseRedirect(reverse('geo-home'))
        return HttpResponseRedirect(reverse('geo-home'))
    return HttpResponseRedirect(reverse('geo-signin'))

#signs out user, pre simple
def signout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('geo-signin'))


def company(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
         companyName = request.POST['name']
         companyEmail = request.POST['email']
         companyType = request.POST['type']
         company=Company.objects.create_Company(company_name=companyName,company_email=companyEmail,company_type=companyType)
         company.save()
         filestore=fileStorage.objects.create_fileStorage(total_file_size="250", used_file_size="0", remaining_file_size="0",company_id=company.pk,company_name=company.company_name)
         return HttpResponseRedirect(reverse('geo-dashboard'))
            # throw error
    return render(request, 'company/index.html',{})


def playground(request):
    return render(request, 'playground/index.html')