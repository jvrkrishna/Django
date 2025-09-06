from django.shortcuts import render

def home(request):
    name = "Rama Krishna"
    friends = ["Ram", "Hari", "Chanti"]
    return render(request, "index.html", {"name": name, "friends": friends})

def about(request):
    return render(request, "about.html")

def contact(request):
    return render(request, "contact.html")

def display(request):
    friends = ["Ram", "Hari", "Chanti"]
    return render(request, "display.html", {"friends": friends})
