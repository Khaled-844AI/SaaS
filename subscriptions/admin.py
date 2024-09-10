from django.contrib import admin

from subscriptions.models import Subscription, UserSubscription, SubscriptionPrice

# Register your models here.
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'active']

admin.site.register(Subscription)
admin.site.register(UserSubscription)
admin.site.register(SubscriptionPrice)

