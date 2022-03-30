import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from apis.business.models import Account, Business
from apis.system_settings.models import Package


class CustomUser(AbstractUser):
    USER_TYPE = (
        ("client", "client"),
        ("client_admin", "client_admin"),
        ("staff", "staff"),
        ("customer", "customer"),
    )
    """custom user model that supports using email instead of username"""
    phone = models.CharField(max_length=50, null=False)
    email = models.EmailField(unique=True)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, null=True)
    business_name = models.CharField(max_length=255, null=True, unique=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True)
    is_verified = models.BooleanField(default=False)
    user_type = models.CharField(choices=USER_TYPE, max_length=20)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email


class UsersVerification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    validity = models.DateTimeField(auto_now_add=True)
    valid = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username