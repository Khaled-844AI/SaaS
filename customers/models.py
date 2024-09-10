from django.db import models
from django.conf import settings
from helpers.billing import create_user
from allauth.account.signals import (
   user_signed_up as allauth_user_signed_up,
   email_confirmed as allauth_email_confirmed,
)
# Create your models here.

User = settings.AUTH_USER_MODEL

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    strip_id = models.CharField(max_length=120, blank=True, null=True)
    init_email = models.EmailField(blank=True, null=True)
    init_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.user.email == "" or not self.user.email is None and not self.strip_id:
            if self.init_email_verified and self.init_email:
                self.strip_id = create_user(name = self.user.username,
                                            email=self.init_email,
                                            metadata={'user_id':self.user.id,
                                                      'username':self.user.username
                                                      })
        super().save(*args, **kwargs)


def allauth_user_signed_up_handler(request, user, **kwargs):
    email = user.email
    Customer.objects.create(
        user=user,
        init_email=email,
        init_email_verified=False,

    )

allauth_user_signed_up.connect(allauth_user_signed_up_handler)


def allauth_email_confirmed_handler(request, email_address, **kwargs):
    qs = Customer.objects.filter(
        init_email=email_address,
        init_email_verified=False,
    )

    for obj in qs:
        obj.init_email_verified = True
        obj.save()

allauth_email_confirmed.connect(allauth_email_confirmed_handler)
