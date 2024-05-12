from django.core.management.base import BaseCommand
from accounts.models import OtpCode
from datetime import datetime, timedelta
from pytz import timezone


class Command(BaseCommand):
    help = "remove all expire otp codes"

    def handle(self, *args, **kwargs):
        tz = timezone("Asia/Tehran")
        expired_time = datetime.now(tz=tz) - timedelta(minutes=2)
        OtpCode.objects.filter(created__lt=expired_time).delete()
        self.stdout.write('all expired otp removed')
