from django.http import HttpResponse
from django.shortcuts import render

def landing_page(request):
    # return HttpResponse("<h1> Find hot papers in your area </h1>")
    return render(request, "index.html")