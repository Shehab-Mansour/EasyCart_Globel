from django.http import HttpResponse
from django.shortcuts import render

from User.views import sinin


# Create your views here.
def home (request):
    return HttpResponse("<h1>Home Page</h1> <dr> <a href=""/user"">user home</a>  <a href=""/user/sinin"">sinin</a> <a href=""/user/login"">login</a> <br> <a href=""/admin"">admin</a>")

