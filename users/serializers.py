from .models import MyUser
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'

    def create(self, validated_data):
        user = MyUser.objects.create_user(
            email = validated_data['email'],
        )
        return user