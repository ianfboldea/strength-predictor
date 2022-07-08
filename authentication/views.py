from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')

        if password != confirmpassword:
            messages.error(request, 'Your username and/or password was not correct.')
            return redirect('signup')

        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = firstname
        myuser.last_name = lastname

        myuser.save()

        messages.success(request, 'Your account has been successfully created.')

        return redirect('signin')

    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username, password)
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            context = {'firstname': user.first_name}
            return render(request, 'authentication/index.html', context)
        else:
            messages.error(request, 'Your username and/or password was not correct.')
            return redirect('authentication:signin')

    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request, 'Logged out succesfully!')
    return redirect('authentication:home')