from datetime import timezone

from django.http.response import HttpResponse
from django.shortcuts import render

from visits.models import PageVist


def home_page(request):
    visits = PageVist.objects.all()
    return render(request, "home.html", context={"visits": visits})