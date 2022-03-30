import uuid
from datetime import timedelta
from django.db import models
from django.utils import timezone
from apis.system_settings.models import Package, Country, State


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255, null=False, unique=True)
    last_payment_date = models.DateTimeField(auto_now_add=True, blank=False)
    next_payment_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(null=False, default=True)

    def __str__(self):
        return self.business_name

    def save(self, *args, **kwargs):
        if self.last_payment_date:
            self.next_payment_date = timezone.now() + timedelta(365)
        super(Account, self).save(*args, **kwargs)


class Business(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    account = models.ForeignKey(Account, max_length=50, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=255, unique=True)
    address = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.store_name