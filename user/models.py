import random
import string
import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


# Create your models here.


class User(AbstractUser):
    pass


class OTPManager(models.Manager):
    def generate(self, data):
        otp = self.model(channel= data['channel'], receiver=data['receiver'])
        otp.save(using=self._db)
        return otp

    def is_valid(self, receiver, request_id, password):
        current_time = timezone.now()
        if self.model.objects.filter(
                receiver=receiver,
                request_id=request_id,
                password=password,
                created__lt=current_time,
                created__gt=current_time - timedelta(seconds=120)
        ).exists():
            return True

def generate_otp():
    rand = random.SystemRandom()
    digits = rand.choices(string.digits, k=4)
    return ''.join(digits)

class OTPRequest(models.Model):
    class OtpChannel(models.TextChoices):
        PHONE = 'phone'
        EMAIL = 'E-mail'


    request_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    channel = models.CharField(max_length=10, choices=OtpChannel.choices, default=OtpChannel.PHONE)
    receiver = models.CharField(max_length=50)
    password = models.CharField(max_length=4, default=generate_otp)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    objects = OTPManager()