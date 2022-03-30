from django.contrib import admin
from .models import Package, Country, State
# Register your models here.

admin.site.register(Package)
admin.site.register(Country)
admin.site.register(State)