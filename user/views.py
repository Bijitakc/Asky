from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

User=get_user_model()

# Create your views here.
def signup(request):
    if request.user.is_authenticated:
        return redirect('chat:index')
    if request.method=="POST":
        errors={}
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password1')
        passwordc=request.POST.get('password2')
        if password!=passwordc :
            errors['top']="Passwords don't match"
        # try:
        exists=User.objects.filter(username=username).first()
        if exists:
            errors['password']="Username already exists"
        if len(errors)>0:
            return render(request,'user/signup.html',context={'errors':errors})
        else:
            print("yes")
            hashed_password=make_password(password)
            user=User(username=username,email=email,password=hashed_password,is_active=True)
            print("it")
            user.save()
            print("is")
            return redirect('user:loginpage')
    else:
        return render(request,'user/signup.html')

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('chat:index')
    if request.method=="POST":
        errors={}
        username=request.POST.get('username')
        password=request.POST.get('upassword')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('chat:index')
        else:
            errors['top']="Wrong Credentials"
        return render(request,'user/login.html',context={'errors':errors})
    else:
        return render(request,'user/login.html')

def logoutpage(request):
    logout(request)
    return redirect('chat:index')