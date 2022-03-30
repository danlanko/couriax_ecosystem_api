from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'category', views.CategoryAPIView)
router.register(r'sub_category', views.SubCategoryAPIView)
router.register(r'supplier', views.SupplierAPIView)
router.register(r'product', views.ProductAPIView)

urlpatterns = [
    path('', include(router.urls)),
    path('product_image/<id>', views.ProductImagesAPIView.as_view()),
]
