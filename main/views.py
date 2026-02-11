from django.shortcuts import render
from django.http import HttpResponse

from .models import *

def hello_view(request):
    return HttpResponse(
    """    
    <H1>Hello World!</H1>
    <hr>
    <p>from view</p>
    """
    )


def home_view(request):
    return render(request, "home.html")

def students_view(request):
    talabalar = Talaba.objects.all()
    data = {
        'talabalar': talabalar,
    }
    return render(request, "students.html", context=data)

def student_details_view(request, student_id):
    talaba = Talaba.objects.get(id=student_id)
    data = {
        'talaba': talaba,
    }
    return render(request, "student.html", context=data)


def mualliflar_view(request):
    mualliflar = Muallif.objects.all()
    context = {
        'mualliflar' : mualliflar,
    }
    return render(request, "mualliflar.html", context)

def muallif_view(request, muallif_id):
    muallif = Muallif.objects.get(id=muallif_id)

    context = {
        'muallif': muallif,
    }
    return render(request, "muallif.html", context)