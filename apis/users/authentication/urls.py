from django.urls import path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('auth/login/', views.UserLoginView.as_view()),
    path('auth/verify/', views.VerificationView.as_view()),
    path('auth/re_verify/', views.ResendVerification.as_view(), name='resend_otp'),
    # Forgot Password uses same views as resend_verification
    path("auth/forgot-password/", views.ResendVerification.as_view(), name="forgot-password"),
    path('auth/forgot_password_validate/', views.ForgotPasswordValidateAPIView.as_view()),
    path('auth/change_password/', views.PasswordChangeAPIView.as_view()),
]
