from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from .forms import *
# Create your views here.
def home(request):
    book = Book.objects.all()
    return render(request, "home.html", {'book':book})

