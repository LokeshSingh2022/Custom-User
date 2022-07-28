from django.contrib import messages
from django.shortcuts import render
from .models import *
from .forms import *
# Create your views here.
def home(request):
    context = {}
    form = ''
    if request.method == "POST":
        form = BookDetails(request.POST, request.FILES)
        if form.is_valid():
            form.save();
            messages.success(request, ('The Book Added Successfully.. !!!'))
        else:
            messages.error(request, 'Error Saving Form')
    context['form'] = form
    return render(request, "account/home.html", context)

def customer(request):
    context = {}
    form = ''
    if request.method == "POST":
        form = CustomerDetails(request.POST , request.FILES )
        if form.is_valid():
            form.save();
            messages.success(request, ('The Customer Added Successfully.. !!!'))
        else:
            messages.error(request, 'Error Saving Form')
    context['form'] = form
    return render(request, "account/customer.html", context)