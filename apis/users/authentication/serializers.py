from rest_framework import serializers
from ..authentication.models import CustomUser as User


class PasswordChangeSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(max_length=50, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'password', 'new_password')
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True},
                        'new_password': {'write_only': True}}

