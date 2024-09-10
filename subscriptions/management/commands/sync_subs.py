from django.core.management import BaseCommand

from subscriptions.models import Subscription


class Command(BaseCommand):

    def handle(self, *args, **options):
        qs = Subscription.objects.filter(active=True)
        for obj in qs:
            for group in obj.groups.all(): # subscription groups
                group.permissions.set(obj.permissions.all())