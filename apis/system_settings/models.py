import uuid
from django.db import models


class Package(models.Model):
    PACKAGE_CHOICE = (
        ("Silver", "Silver"),
        ("Bronze", "Bronze"),
        ("Gold", "Gold")
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=255, null=True, choices=PACKAGE_CHOICE)
    amount = models.DecimalField(max_digits=50, blank=True, null=True, decimal_places=2)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Package"
        verbose_name_plural = "Packages"


class AccountPersonified(models.Model):
    class Meta:
        """
        Personifying premium accounts
        """


class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50)
    currency = models.CharField(max_length=50)
    code = models.CharField(max_length=3)
    unicode = models.CharField(max_length=5, null=True, blank=True)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"


class State(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "State"
        verbose_name_plural = "States"
