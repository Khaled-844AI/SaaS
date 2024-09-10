from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.conf import settings


# Create your views here.
LOGIN_URL = settings.LOGIN_URL


@staff_member_required(login_url=LOGIN_URL)
def profiles_list(request):
    context = {
        'user_objects': User.objects.filter(is_active=True)
    }
    return render(request , 'profiles/list.html', context=context)


@login_required
def profile_detail_view(request, username):
    user = request.user
    print(
        user.has_perm('subscriptions.basic'),
        user.has_perm('subscriptions.pro'),
        user.has_perm('subscriptions.advanced'),
        user.has_perm('subscriptions.basic_ai'),
          )
    user_groups = user.groups.all()
    if user_groups.filter(name__icontains='basic').exists():
        return HttpResponse("Congrats !!!")
    profile_user = get_object_or_404(User, username=username)
    owner = profile_user == user
    context = {
        'object':profile_user,
        'instance':profile_user,
        'owner':owner,
    }
    return render(request ,'profiles/detail.html', context=context)
