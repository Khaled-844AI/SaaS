from django.contrib import admin

from subscriptions.models import Subscription, UserSubscription, SubscriptionPrice

class SubscriptionPricing(admin.TabularInline):
    model = SubscriptionPrice
    readonly_fields = ['stripe_id']
    can_delete = False
    extra = 0

# Register your models here.
class SubscriptionAdmin(admin.ModelAdmin):
    inlines = [SubscriptionPricing]
    list_display = ['name', 'active']

admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(UserSubscription)
admin.site.register(SubscriptionPrice)

