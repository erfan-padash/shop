from utils import send_otp_code
from celery import shared_task
from datetime import datetime, timedelta
from pytz import timezone
from .models import OtpCode


def otp_send_task(phone_number, code):
    send_otp_code(phone_number, code)


@shared_task
def delete_expire_otp_codes_task():
    tz = timezone("Asia/Tehran")
    expired_time = datetime.now(tz=tz) + timedelta(minutes=2)
    OtpCode.objects.filter(created__lt=expired_time).delete()