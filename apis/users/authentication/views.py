from random import randint
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from rest_framework import views, permissions, serializers, response, status, generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt import tokens
from apis.users.authentication.models import UsersVerification
from django.utils import timezone
from .models import CustomUser as User
from .serializers import PasswordChangeSerializer
from ...helpers.notification import send_activation_code


class UserLoginView(views.APIView):
    permission_classes = (AllowAny,)
    http_method_names = ['post', ]

    @staticmethod
    def post(request):
        email = request.data.get("email", "")
        password = request.data.get("password", "")
        try:
            user_object = User.objects.get(email=email)
        except User.DoesNotExist:
            return response.Response(
                {
                    "message": "failure",
                    "data": "null",
                    "error": {"email": "Email does not exist"},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(email=user_object.email, password=password)
        if not user:
            return response.Response(
                {
                    "message": "failure",
                    "data": "null",
                    "error": {"password": "Incorrect password"},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not user.is_verified:
            return response.Response(
                {
                    "message": "failure",
                    "data": "null",
                    "error": {"email": "Email is not yet verified"},
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        token = tokens.AccessToken.for_user(user)
        return response.Response(
            {
                "message": "success",
                "data": {"token": str(token)},
                "errors": "null",
            },
            status=status.HTTP_200_OK,
        )


class VerificationView(views.APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        with transaction.atomic():
            try:
                email = self.request.data['email']
                otp = self.request.data['otp']
                user = User.objects.get(email=email)
                user_otp = UsersVerification.objects.get(user=user, valid=True)
                if otp == user_otp.code:
                    difference = timezone.now() - user_otp.validity
                    if difference.total_seconds() > 120:  # Invalidate OTP if more than 2 minutes
                        raise serializers.ValidationError({
                            'details': ['Verification code expired']
                        })
                    user_otp.valid = False
                    user.is_active = True
                    user.is_verified = True
                    user.last_login = timezone.now()
                    user.save()
                    user_otp.save()
                else:
                    raise serializers.ValidationError({
                        "details": ["Code is invalid"]
                    })
            except UsersVerification.DoesNotExist:
                raise serializers.ValidationError({
                    "details": ['Invalid OTP']
                })
            except User.DoesNotExist:
                raise serializers.ValidationError({
                    "details": ["A user with this email does not exist"]
                })
            except KeyError as error:
                raise serializers.ValidationError({
                    "details": [f'required {error}']
                })

            token = tokens.AccessToken.for_user(user)

            return response.Response({
                "message": "success",
                "data": {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "verified": user.is_verified,
                    "data": {"token": str(token)},
                }
            }, status=status.HTTP_200_OK)


class ResendVerification(views.APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        with transaction.atomic():
            try:
                email = self.request.data['email']
                user = User.objects.get(email=email)
                send_activation_code(user=user)
            except Exception as error:
                raise serializers.ValidationError({
                    "details": error
                })

            return response.Response({
                "success": True,
                "msg": "Verification message sent"
            }, status=status.HTTP_200_OK)


# Forgot Password OTP Verification
class ForgotPasswordValidateAPIView(views.APIView):
    permission_classes = [permissions.AllowAny, ]

    def post(self, request):
        try:
            email = self.request.data['email']
            otp = self.request.data['otp']
            password = self.request.data['password']
            user = User.objects.get(email=email)
            user_otp = UsersVerification.objects.get(user=user, valid=True)

            if otp == user_otp.code:
                difference = timezone.now() - user_otp.validity.replace()
                if difference.total_seconds() > 120:  # Invalidate OTP if more than 2 minutes
                    raise serializers.ValidationError({
                        'details': ['Verification code expired']
                    })
                user_otp.valid = False
                validate_password(self.request.data["password"])
                user.set_password(raw_password=password)
                user.save()
                user_otp.save()
            else:
                raise serializers.ValidationError({
                    "details": ["Code is invalid"]
                })
        except UsersVerification.DoesNotExist:
            raise serializers.ValidationError({
                "details": ['Invalid OTP']
            })
        except User.DoesNotExist:
            raise serializers.ValidationError({
                "details": ["User with input credentials cannot be found"]
            })
        except KeyError as error:
            raise serializers.ValidationError({
                "details": [f'required {error}']
            })

        return response.Response({
            'success': True,
            'message': "Password has been changed successfully"
        })


class PasswordChangeAPIView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch']
    serializer_class = PasswordChangeSerializer
    queryset = User.objects.all()
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        user = self.request.user
        try:
            if not user.check_password(self.request.data["password"]):
                raise serializers.ValidationError({
                    'password': ['Your old password is incorrect']
                })
        except Exception as error:
            raise serializers.ValidationError({
                'details': ['Your old password is incorrect']
            })
        try:
            validate_password(self.request.data["new_password"])
        except Exception as error:
            raise serializers.ValidationError({
                'details': error
            })
        try:
            user.set_password(self.request.data["new_password"])
            user.save()
        except Exception as error:
            print(error)
        return response.Response({
            'password': ['password changed successfully']
        })