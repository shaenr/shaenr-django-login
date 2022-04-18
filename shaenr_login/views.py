from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.
def index_page(request):
    return HttpResponse("Index page.")