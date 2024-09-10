from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect


# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request , username = username , password = password)
        if user is not None:
            login(request, user)
            return redirect("/")
    return render(request, 'auth/login.html', {})


def register_view(request):
    return render(request, 'auth/register.html', {})



def logout_view(request):
    logout(request)
    return render(request, 'auth/logout.html', {})


