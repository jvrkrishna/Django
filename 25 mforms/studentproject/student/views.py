from django.shortcuts import render
from .forms import StudentForm
def student_view(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()   # saves data to database
            return render(request, 'success.html')
    else:
        form = StudentForm()

    return render(request, 'student.html', {'form': form})