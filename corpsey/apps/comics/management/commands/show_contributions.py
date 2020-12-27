from datetime import datetime, timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from corpsey.apps.comics.models import Contribution

class Command(BaseCommand):
    help = 'Checks status of contributions'

    def handle(self, *args, **options):
        contributions_expiring_tomorrow = Contribution.objects.filter(pending=True, has_panels=False, deadline__lte=timezone.now()+timedelta(days=1))
        contributions_expired = Contribution.objects.filter(pending=True, has_panels=False, deadline__lte=timezone.now())
        self.stdout.write(self.style.SUCCESS('Contributions expiring tomorrow: '))
        for c in contributions_expiring_tomorrow:
            self.stdout.write("%s %s (%s)" % (c.id, c, c.deadline))
            self.stdout.write("%s" % timezone.now())
            self.stdout.write("%s" % (timezone.now() + timedelta(days=1)))
        self.stdout.write('--');
        self.stdout.write(self.style.SUCCESS('Contributions expired: '))
        for c in contributions_expired:
            self.stdout.write("%s (expired %s)" % (c, c.deadline))
