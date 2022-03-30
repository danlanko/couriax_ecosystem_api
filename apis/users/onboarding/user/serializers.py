from django.contrib.auth import password_validation
from rest_framework import serializers
from apis.business.models import Account
from apis.helpers.notification import send_activation_code
from apis.users.authentication.models import CustomUser as User


class UserOnboardSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "phone", "business_name", "package", "email", "password",)

    def get_fields(self):
        fields = super(UserOnboardSerializer, self).get_fields()
        for field in fields.values():
            field.required = True
        return fields

    def create(self, validated_data):
        package = validated_data['package']
        business_name = validated_data['business_name']
        password = validated_data.pop('password')
        new_account = Account.objects.create(
            package=package,
            business_name=business_name,
        )
        new_account.save()
        try:
            password_validation.validate_password(password=password)
            user = User(**validated_data, username=validated_data["email"], is_active=False, account=new_account,
                        user_type="client_admin", )
            user.set_password(password)  # Necessary so that raw_text password can hashed before saving into DB
            user.save()
            send_activation_code(user)
        except Exception as error:
            raise serializers.ValidationError({
                "details": [error]
            })
        return validated_data


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('phone', )

