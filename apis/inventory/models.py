import uuid
from django.db import models
from apis.products.models import Product, Business
from apis.users.authentication.models import CustomUser as User


class InventoryLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    previous_qty = models.IntegerField(null=True)
    is_in = models.BooleanField()
    remark = models.TextField()
    performed_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    is_system = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)