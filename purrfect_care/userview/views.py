from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request : HttpRequest):
    return HttpResponse("Purrfect Care")
# Create your views here.
