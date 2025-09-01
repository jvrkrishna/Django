from django.shortcuts import render

# Create your views here.
def addAdmission(request):
    return render(request, 'App1/add-admission.html')

def admissionReport(request):
    return render(request, 'App1/admission-report.html')