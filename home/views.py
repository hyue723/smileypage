from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    context = {} #information that I am going to pass in
    return render(request, "home/homepage.html", context)

def tutorial(request):
    context = {}
    return render(request, 'home/tutorial.html', context)

def about(request):
    context = {}
    return render(request, 'home/about.html', context)