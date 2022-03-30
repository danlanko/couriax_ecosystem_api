from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
# router.register(r'product', views.ProductAPIView)

urlpatterns = [
    # path('', include(router.urls)),
    path('inventory/', views.InventoryLogAPIView.as_view()),
]
