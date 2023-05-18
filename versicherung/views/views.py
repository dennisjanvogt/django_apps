from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url="login")
def home(request: HttpRequest):
    context = {}
    return render(request, "home.html", context)
