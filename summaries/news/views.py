from django.shortcuts import render
from django.http import HttpResponse


def mainPage(request):
    return HttpResponse("главная страница ")
