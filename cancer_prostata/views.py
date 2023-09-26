from django.shortcuts import render
from django.http import HttpResponse

def login(request):
    return render(request, "login.html", {})

def login2(request):
    return render(request, "login2.html", {})