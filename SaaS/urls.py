"""
URL configuration for SaaS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from UserAuth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name="home-page"),
    path('login/', auth_views.login_view , name = "login"),
    path('logout/', auth_views.logout_view , name = "logout"),
    path('register/', auth_views.register_view, name="register"),
    path('accounts/', include('allauth.urls')),
    path('profiles/', include('profiles.urls')),
    path('subscriptions/', include('subscriptions.urls')),
    path('checkout/', include('checkouts.urls')),

    path('protected/staff-only' , views.staff_page , name="protected"),
]
