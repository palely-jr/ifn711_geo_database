from django.db.models import Sum
from django.http.response import FileResponse
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Items, fileStorage, Company, UserCompanyRelationship, SharedItems
from django.core.mail import EmailMessage
from django.urls import reverse
from .viewsmethods import geolocater
from geopy.geocoders import Nominatim


# basic homepage --> needs to be done
def home(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)
        if request.method == 'GET':
            search = request.GET.get('search_term', False)
            if search:
                user_items = Items.objects.filter(user_id=user.pk, item_file__icontains=search)
                return render(request, 'index/home.html', {'user_items': user_items})
        # need to get all items with user.id and then put in context and put into the frontend
    return render(request, 'index/home.html')


def search(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            return render(request, 'index/home.html')
        return HttpResponseRedirect(reverse('geo-home'))
    return HttpResponseRedirect(reverse('geo-signin'))


def signin(request):
    # use this to authenticate each request made
    if request.user.is_authenticated:
        return redirect('geo-dashboard')
    # this to post
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST["password"]
        # we use this to authenticat the user
        user_account = authenticate(username=username, password=password)
        print("this is something", user_account)
        # check if user is authenticated
        if user_account:
            if user_account.is_active:
                login(request, user_account)
                return HttpResponseRedirect(reverse('geo-dashboard'))
            # throw error
            else:
                return render(request, 'signin/signin.html', {
                    'login_disabled': 'account disabled'
                })
        # pass through different error messages for error validation on client side
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
                # do a for loop and delete each
                for item in item_list:
                    print("this is item: ", item)
                    Items.objects.filter(item_id=item).delete()
                return HttpResponseRedirect(reverse('geo-home'))
        return HttpResponseRedirect(reverse('geo-home'))
    return HttpResponseRedirect(reverse('geo-signin'))


# register user form
def companyregistration(request):
    # no user needs to be logged in
    if request.method == 'POST':
        # do some data stuff
        orgName = request.POST['organisation_name']
        orgEmail = request.POST['organisation_email']
        company = Company.objects.create_Company(company_name=orgName, company_email=orgEmail)
        company.save()
        return HttpResponseRedirect(reverse('geo-playground'))
    else:
        return render(request, 'company_registration/CompanyRegistration.html', {})


## we
def register(request):
    companyDetails = Company.objects.all()
    companyNames = []
    for companyId in companyDetails:
        companyNames.append(companyId.company_name)

    print(companyNames)

    if request.method == 'POST':
        # data cleaning
        # assignment
        username = request.POST['username']
        name = request.POST['name']
        # end assignment
        password = request.POST['passwordOne']
        # you dont need to put each POST form element into a variable
        # i just found it more readable
        # ----------------
        # so want to check that the organisation exists, if so can add otherwise, dont

        orgName = request.POST.getlist('Organisation')

        # check for the company existence
        company_exists = Company.objects.check_company(orgName)
        if (company_exists):
            # store them as a user, in mysql auth_user is the best user table for us
            user = User.objects.create_user(username=username, first_name=name, email=username, password=password,
                                            last_name="1")  # creating a file storage for new user

            user.is_active = True
            user.save()
            company_id = Company.objects.get(company_name=orgName[0])
            newUser = User.objects.get(username=username)
            # print("company id is: ", company_id.id)

            # also need to create the relationship between company and user
            company_user = UserCompanyRelationship.objects.create_relationship(company_id=company_id,
                                                                               user_id=newUser.pk)
            company_user.save()
            # want to setup the filestorageallocation

            fileStorageExist = fileStorage.objects.filter(company_id=company_id);

            if fileStorageExist:
                print("Storage already allocated")
            else:
                i_file_store = fileStorage.objects.create_initial_storage(250, 0, company_id=company_id,
                                                                          company_name=orgName[0])
                # i_file_store.save()

            # redirect back to signin page, check geo_database.urls to see the names (im using a geo-xxx ..
            # naming convention)
            return HttpResponseRedirect(reverse('geo-signin'))
    else:
        # user = User.objects.create_user(username="warwick@orefox.com", first_name="Warwick Anderson", email="warwick@orefox.com", password="password",  last_name="1",is_superuser="1")       #creating a file storage for new admin user
        # user.save();
        return render(request, 'registration/registration.html', {"company_names": companyNames})

def sharefiles(request, item_id):
    if request.user.is_authenticated:
        #share the file with a company
        if request.method == 'POST':
            shared_file_id = item_id
            orgName = request.POST.getlist('Organisation')[0]

            shared_company = Company.objects.get(company_name=orgName)
            item = Items.objects.get(item_id=shared_file_id)
            current_company = Company.objects.get(id=item.company_id)

            shared_item = SharedItems.objects.create_shared_items(current_company, shared_company, item)
            shared_item.save()

            #success
            return HttpResponseRedirect(reverse('geo-dashboard'))
        else:
            companyDetails = Company.objects.all()
            companyNames = []
            for companyId in companyDetails:
                companyNames.append(companyId.company_name)
            item = Items.objects.get(item_id=item_id)
            return render(request, 'sharedfile/sharedfile.html', {"item_id": item_id, "company_names": companyNames, "item": item})
    else:

        return redirect('geo-register')


def mapall(request):
    #map all the files under the company
    if request.user.is_authenticated:
        #alright
        #all items associated with the users company

        #we get the user
        user = User.objects.get(username=request.user.username)

        company = UserCompanyRelationship.objects.get(user_id=user.pk)

        items = Items.objects.all().filter(company_id=company.company_id)
        for item in items:
            print(item.item_name)

        shared = SharedItems.objects.all().filter(company_shared=company.company_id)
        # do a loop and push into an array
        # dictionary
        itemDictionary = {}

        for item in shared:
            # print(item.company_current.company_name)
            newItem = Items.objects.get(item_id=item.item_id)
            # print(item.company_current.company_name)
            itemDictionary[item] = newItem

        return render(request, 'maps/allmaps.html', {"items": items, "sharedFiles": itemDictionary})
    else:
        return redirect('geo-signin')


def mapsingle(request, item_id):

    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)

        company = UserCompanyRelationship.objects.get(user_id=user.pk)
        item = Items.objects.get(item_id=item_id)
        return render(request, 'maps/singlemap.html', {"item": item})

def removeshare(request, item_id, company_name):
    if request.user.is_authenticated:

        #do something
        hello = "hello"
        if request.method == 'POST':
            print("this worked: ", company_name)
            print("this worked: ", company_name)
            username = request.user.username
            user = User.objects.get(username=username)
            print(user.pk)
            # pulling file details
            # get the company id in the relationship table
            company = UserCompanyRelationship.objects.get(user_id=user.pk)
            current_company = Company.objects.get(id=company.company_id)
            shared_company = Company.objects.get(company_name=company_name)
            #in sql terms
            #we want to DELETE FROM users WHERE company.company_id = company_id AND

            #usually you want cleanup code on delete --- we do not have due to size of project
            SharedItems.objects.filter(company_current=current_company.id,
                                                      item_id=item_id,
                                                      company_shared=shared_company).delete()
            return redirect('geo-dashboard')
        else:
            #do the get request
            return render(request, 'remove/shared.html', {"item_id": item_id,
                                                          "company_name": company_name})
    else:
        return redirect('geo-signin')

def dashboard(request):
    print("this is touched")
    if request.user.is_authenticated:
        if request.user.is_superuser:
            username = request.user.username
            user = User.objects.get(username=username)
            return render(request, 'dashboard/admin/index.html', {'user_items': username})
        else:
            username = request.user.username
            user = User.objects.get(username=username)
            print(user.pk)
            # pulling file details
            # get the company id in the relationship table
            company = UserCompanyRelationship.objects.get(user_id=user.pk)
            print("COMPANY RELATIONSHIP \n\n\n")
            print(company.company_id)
            print("end of company relationship  \n\n\n\n\n")
            # then find the releveant file details
            fileDetails = fileStorage.objects.get(company_id=company.company_id)

            listFileDetails = [fileDetails.total_file_size, fileDetails.used_file_size, fileDetails.remaining_file_size]

            companyInformation = Company.objects.get(id=company.company_id)

            #company name, employee name
            companyDetails = [companyInformation.company_name, user.first_name]

            #obtain all items associated with company id and user ..
            items = Items.objects.all().filter(company_id=company.company_id)

            #also need to check for shared files
            shared = SharedItems.objects.all().filter(company_shared=company.company_id)
            #do a loop and push into an array
            #dictionary
            itemDictionary = {}

            for item in shared:
                # print(item.company_current.company_name)
                newItem = Items.objects.get(item_id=item.item_id)
                # print(item.company_current.company_name)
                itemDictionary[item] = newItem

            #items without appending

            #also need to check for my shared files and display so i can remove them
            currentSharedItems = SharedItems.objects.all().filter(company_current=company.company_id)
            myShared = []
            for currentShared in currentSharedItems:
                #find the object with the current company id
                item = Items.objects.get(item_id=currentShared.item_id)

                #give the item a shared company
                item.shared_company = currentShared.company_shared.company_name
                #append it to the list to send to the frontend
                myShared.append(item)
            # create a list for filedetails
            for item in myShared:
                print(item.company_id)
        # information that needs to be passed over to the front end
        # file details
        # company information
        return render(request, 'dashboard/index.html', {'user_name': user.first_name,
                                                        "file_details": listFileDetails,
                                                        "company_details": companyDetails,
                                                        "items": items,
                                                        "sharedItems": itemDictionary,
                                                        "myShared": myShared})
    else:
        return render(request, 'signin/signin.html')


#use this for getting geolocation

def filestoragealoc(request):
    if request.user.is_authenticated:
        # pulling file details
        fileDetails = fileStorage.objects.all()
        companyIds = []
        for companyId in fileDetails:
            companyIds.append(int(companyId.company_id))

        print("this is", companyIds)
        if request.method == 'POST':
            company_id = request.POST['userid']
            size = request.POST['size']

            try:
                int(company_id)
                id_int = True
            except ValueError:
                id_int = False

            try:
                int(size)
                size_int = True
            except ValueError:
                size_int = False

            if id_int and size_int:
                exists = int(company_id) in companyIds
                if exists:
                    fileDetail = fileStorage.objects.get(company_id=company_id)
                    if fileDetail:
                        fileDetail.total_file_size = size
                        fileDetail.save()
                        return HttpResponseRedirect(reverse('geo-filestoragealoc'))
                        # throw error
                    else:
                        return render(request, 'signin/signin.html', {
                            'invalid': 'Please Input Valid Login'
                        })
        return render(request, 'filestorage/index.html', {'filedetails': fileDetails})
    else:
        return render(request, 'signin/signin.html')


def uploadItem(request):
    print("this is accessed")
    if request.user.is_authenticated:
        if request.method == 'POST':
            # need to recheck this to the
            uploaded_file = request.FILES['myFile']
            address = request.POST['address']
            print("\n\n\n\n")
            print(uploaded_file.size)
            print("\n\n\n\n")
            file_name = request.POST['filename']
            username = request.user.username
            print(username)
            user = User.objects.get(username=username)
            print(user.pk)
            user_company = UserCompanyRelationship.objects.get(user_id=user.pk)
            company = Company.objects.get(id=user_company.company_id)
            geolocation = Nominatim(user_agent="geo_database")
            location = geolocation.geocode(address)
            new_item = Items.objects.create_item(item_file=uploaded_file, item_name=file_name, company_id=company, item_long=location.longitude, item_lat=location.latitude)
            new_item.save()
            return HttpResponseRedirect(reverse('geo-dashboard'))
        return render(request, 'fileupload/uploadindividual.html', {"success": "upload file"})
    return HttpResponseRedirect(reverse('geo-signin'))


# signs out user, pre simple
def signout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse('geo-signin'))


def company(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            companyName = request.POST['name']
            companyEmail = request.POST['email']
            company = Company.objects.create_Company(company_name=companyName, company_email=companyEmail)
            company.save()
            # filestore=fileStorage.objects.create_fileStorage(total_file_size="250", used_file_size="0", remaining_file_size="0",company_id=company.pk,company_name=company.company_name)
            return HttpResponseRedirect(reverse('geo-dashboard'))
            # throw error
    return render(request, 'company/index.html', {})


def playground(request):
    user = User.objects.get(username="jesse_studin")
    company = Company.objects.get(company_name="orefox")
    user_company_name = UserCompanyRelationship.objects.get(user_id=user.pk)
    print(user_company_name.company_id)

    return render(request, 'playground/index.html', {'company': user_company_name})
