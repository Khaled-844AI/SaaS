from django.contrib.auth.models import Group, Permission
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save

from helpers.billing import create_product, create_price

# Create your models here.
User = settings.AUTH_USER_MODEL
ALLOW_CUSTOM_GROUPS = True

class Subscription(models.Model):
    name = models.CharField(max_length=120)
    active = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group)
    permissions = models.ManyToManyField(Permission,
                                         limit_choices_to={'content_type__app_label': 'subscriptions',
                                                           'codename__in': [
                                                               'basic',
                                                               'advanced',
                                                               'pro',
                                                               'basic_ai',
                                                           ]})
    strip_id = models.CharField(max_length=120, blank=True, null=True)

    class Meta:
        permissions = [
            ('advanced', 'Advanced Perm'),
            ('pro', 'Pro Perm'),
            ('basic', 'Basic Perm'),
            ('basic_ai', 'Basic_AI Perm')
        ]

    def save(self, *args, **kwargs):
        if not self.strip_id:
            self.strip_id = create_product(name = self.name,
                                        metadata={'subscription_id':self.id,
                                                    })
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

from django.db import models

class SubscriptionPrice(models.Model):
    class IntervalChoice(models.TextChoices):
        MONTHLY = 'month', 'Monthly'
        YEARLY = 'year', 'Yearly'

    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, blank=True, null=True)
    strip_id = models.CharField(max_length=120, blank=True, null=True)
    interval = models.CharField(
        max_length=120,
        choices=IntervalChoice.choices,  # Correct usage of choices
        default=IntervalChoice.MONTHLY
    )
    price = models.DecimalField(max_digits=10, decimal_places=2,default=99.99)


    def __str__(self):
        if self.subscription is None:
            return None
        return f'{self.subscription.name} -- {self.subscription.name}'

    @property
    def stripe_currency(self):
        return "usd"

    @property
    def product_strip_id(self):
        if not self.subscription:
            return None
        return self.strip_id

    @property
    def stripe_price(self):
        return self.price * 100

    def save(self, *args, **kwargs):
        if self.strip_id is None and self.product_strip_id is not None:

            self.strip_id = create_price(
                currency=self.stripe_currency,
                unit_amount=self.stripe_price,
                recurring={"interval": self.interval},
                product=self.product_strip_id,
                metadata={
                    'subscription_price_id': self.id,
                }
            )


class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.subscription is None:
            return f'{self.user}'
        return f'{self.user} -- {self.subscription.name}'


def user_sub_post_save(sender, instance, *args, **kwargs):
    user_sub_instance = instance
    user = user_sub_instance.user
    subscription_obj = user_sub_instance.subscription
    groups_ids = []
    if subscription_obj is not None:
        groups = subscription_obj.groups.all()
        groups_ids = groups.values_list('id', flat=True)
    if not ALLOW_CUSTOM_GROUPS:
        user.groups.set(groups_ids)
    else:
        subs_qs = Subscription.objects.filter(active=True)
        if subscription_obj is not None:
            subs_qs = subs_qs.exclude(id=subscription_obj.id)
        subs_groups = subs_qs.values_list("groups__id", flat=True)
        current_groups = user.groups.all().values_list('id', flat=True)
        final_group_ids = list(set(groups_ids) | set(current_groups) - set(subs_groups))
        user.groups.set(final_group_ids)


post_save.connect(user_sub_post_save, sender=UserSubscription)