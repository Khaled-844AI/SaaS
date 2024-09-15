from django.contrib.auth.models import Group, Permission
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.urls import reverse

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
    stripe_id = models.CharField(max_length=120, blank=True, null=True)
    order = models.IntegerField(default=-1)
    featured = models.BooleanField(default=True, help_text='Django feature pricing')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    features = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['order', 'featured', '-updated']
        permissions = [
            ('advanced', 'Advanced Perm'),
            ('pro', 'Pro Perm'),
            ('basic', 'Basic Perm'),
            ('basic_ai', 'Basic_AI Perm')
        ]

    def save(self, *args, **kwargs):
        if not self.stripe_id:
            self.stripe_id = create_product(name = self.name,
                                        metadata={'subscription_id':self.id,
                                                    })
        super().save(*args, **kwargs)

    def get_features_as_list(self):
        if self.features:
            return [x.strip() for x in self.features.split('\n')]
        return []

    def __str__(self):
        return self.name


class SubscriptionPrice(models.Model):
    class IntervalChoice(models.TextChoices):
        MONTHLY = 'month', 'Monthly'
        YEARLY = 'year', 'Yearly'

    subscription = models.ForeignKey(Subscription, on_delete=models.SET_NULL, blank=True, null=True)
    stripe_id = models.CharField(max_length=120, blank=True, null=True)
    interval = models.CharField(
        max_length=120,
        choices=IntervalChoice.choices,  # Correct usage of choices
        default=IntervalChoice.MONTHLY
    )
    price = models.DecimalField(max_digits=10, decimal_places=2,default=99.99)
    order = models.IntegerField(default=-1)
    featured = models.BooleanField(default=True, help_text='Django feature pricing')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['subscription__order' ,'order', 'featured', '-updated']


    def __str__(self):
        if self.subscription is None:
            return None
        return f'{self.subscription.name} -- {self.price}'

    def get_checkout_url(self):
        return reverse('sub-price-checkout', kwargs={'price_id':self.id})

    @property
    def display_features(self):
        if not self.subscription:
            return []
        return self.subscription.get_features_as_list()

    @property
    def stripe_currency(self):
        return "usd"

    @property
    def product_stripe_id(self):
        if not self.subscription:
            return None
        return self.subscription.stripe_id

    @property
    def stripe_price(self):
        return int(self.price * 100)

    def save(self, *args, **kwargs):
        if not self.stripe_id and self.product_stripe_id is not None: # no price but the product is available
            self.stripe_id = create_price(
                currency=self.stripe_currency,
                unit_amount=self.stripe_price,
                recurring={"interval": self.interval},
                product=self.product_stripe_id,
                metadata={
                    'subscription_price_id': self.id,
                }
            )
        super().save(*args, **kwargs)
        if self.featured and self.subscription:
            qs = SubscriptionPrice.objects.filter(
                subscription=self.subscription,
                interval=self.interval
            ).exclude(id=self.id)
            qs.update(featured=False)



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
        current_user_groups = user.groups.all().values_list('id', flat=True)
        final_group_ids = list(set(groups_ids) | set(current_user_groups) - set(subs_groups))
        user.groups.set(final_group_ids)


post_save.connect(user_sub_post_save, sender=UserSubscription)