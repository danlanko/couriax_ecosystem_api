from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'register', views.UserOnboarding)

urlpatterns = [
    path('', include(router.urls)),
    # path('register', views.UserOnboarding.as_view()),
]
