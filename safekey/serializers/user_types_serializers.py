from safekey.models import UserType
from rest_framework import serializers

class UsersTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = '__all__'