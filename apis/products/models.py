import uuid
from django.db import models
from apis.business.models import Business, Account
from apis.system_settings.models import Country


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    business = models.ForeignKey(Business, max_length=50, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Supplier(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255,)
    phone = models.CharField(max_length=255,)
    email = models.EmailField(max_length=255)
    contact_person = models.CharField(max_length=255,)
    contact_phone = models.CharField(max_length=255,)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255,)
    sku = models.CharField(max_length=50)
    barcode = models.CharField(max_length=50, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True)
    cost_price = models.DecimalField(decimal_places=2, max_digits=50)
    sales_price = models.DecimalField(decimal_places=2, max_digits=50)
    stock_unit = models.IntegerField(default=0, help_text="Quantity remaining in stock")
    unit_measurement = models.CharField(max_length=255, null=True,
                                        help_text="Unit of measuring the item EG: grams, module, etc.. ")
    unit_increment = models.CharField(max_length=255, null=True,
                                      help_text="Unit of increment while adding to card, EG: 0.5, 1")
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(null=True)
    image = models.ImageField(upload_to='product_images', null=True)

    class Meta:
        unique_together = (('sku', 'business'), )

    def __str__(self):
        return self.name


