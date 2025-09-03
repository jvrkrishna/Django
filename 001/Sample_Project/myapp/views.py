from django.shortcuts import render

# Create your views here.
def static_example(request):
    return render(request, "myapp/static_example.html")