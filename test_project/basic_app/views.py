from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from basic_app.forms import UserProfileInfoForm, UserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    return render(request,'index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    user_form = UserForm()
    profile_form = UserProfileInfoForm()
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password) #hashes password
            user.save
            profile = profile_form.save(commit=False)
            profile.user = user #this step makes the relation between the user in its document and his profile things in the profile document
            
            if 'profile_pic' in request.FILES.keys():
                profile.profile_pic = request.FILES['profile_pic'] #this step gives value for profile.profile_pic
                
            profile.save() #this step saves the profile things to profile document
            registered=True
            print(user, profile)

        else:
            return HttpResponse('Form is invalid!')
    return render(request,'registeration.html',{'user_form':user_form,
                                                'profile_form':profile_form,
                                                'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username='username', password='password')
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
        
        else:
            return HttpResponse("Login Failed")
    else:
        return render(request,'login.html')
    

