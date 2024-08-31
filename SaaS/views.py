from django.http.response import HttpResponse


def home_page(request):

    return HttpResponse("<h1>Hello word </h1>")