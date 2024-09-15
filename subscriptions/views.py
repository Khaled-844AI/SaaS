from django.shortcuts import render
from django.urls import reverse

from subscriptions.models import Subscription, SubscriptionPrice


# Create your views here.


def subscription_pricing_view(request, interval="month"):
    qs = SubscriptionPrice.objects.filter(featured=True)
    obj_list = qs.filter(
        interval=interval,
    )
    url = "pricing_interval"
    month_url = reverse(url, kwargs={"interval": "month"})
    year_url = reverse(url, kwargs={"interval":"year"})

    return render(request, 'subscriptions/pricing.html',{
        "obj_list":obj_list,
        "month": True if interval == "month" else False,
        "month_url":month_url,
        "year_url":year_url,
    })
