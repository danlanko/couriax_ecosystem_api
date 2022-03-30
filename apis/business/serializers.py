from rest_framework import serializers
from apis.business.models import Business


class BusinessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Business
        exclude = ('account', )


class BusinessUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Business
        fields = ('address', )