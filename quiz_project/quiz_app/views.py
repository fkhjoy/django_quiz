from django.shortcuts import render
from django.http import HttpResponse

def home(request):

    return HttpResponse("<h1>Welcome To Quiz</h1>")

def login(request):

    return render(request, 'quiz_app/login.html')
