from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CreateUserForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate

def home(request):

    return HttpResponse("<h1>Welcome To Quiz</h1>")

def signup(request):

    if request.method == 'GET':
        return render(request, 'quiz_app/signup.html', {'form': CreateUserForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except:
                return render(request, 'quiz_app/signup.html', {'form': CreateUserForm, 'error': "User already exists"}, status=400)
        else:
            return render(request, 'quiz_app/signup.html', {'form': CreateUserForm, 'error': "Password didn't match"}, status=400)


def login(request):

    if request.method == 'GET':
        return render(request, 'user_authentication/login_user.html', {'form': AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if not user:
            return render(request, 'user_authentication/login_user.html', {'form': AuthenticationForm, 'error': 'User not found'})
        else:
            login(request, user)
            return redirect('home_dashboard')


def logout_user(request):
    logout(request)
    return redirect('login')
