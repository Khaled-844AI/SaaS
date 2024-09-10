from datetime import timezone

from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

from django.shortcuts import render

from visits.models import PageVist

LOGIN_URL=settings.LOGIN_URL
@login_required
def home_page(request):
    visits = PageVist.objects.all()
    user = request.user
    return render(request, "home.html", context={"visits": visits, "user": user})


@staff_member_required(login_url=LOGIN_URL)
def staff_page(request):
    return render(request, 'protected/user-only.html', {})


