from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        # token['profile_image'] = user.profile_image
        token['username'] = user.username
        token['email'] = user.email
        # token['phone'] = user.phone
        token['gender'] = user.gender
        # token['nationality'] = user.nationality
        # token['date_joined'] = user.date_joined
        token['is_verified'] = user.is_verified
        token['is_active'] = user.is_active

        # ...

        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # print(validated_data)
        groups_data = validated_data.pop('groups', None)
        user_permissions_data = validated_data.pop('user_permissions', None)
        password = validated_data.pop('password', None)

        instance = self.Meta.model(**validated_data)
        # print(instance)
        instance.set_is_active(True)

        if password is not None:
            instance.set_password(password)
            # instance.set_visible_password(password)
        # print(instance)
        instance.save()
        if groups_data is not None:
            instance.groups.set(groups_data)  # Use the set() method to set the many-to-many relationship
        
        if user_permissions_data is not None:
            instance.user_permissions.set(user_permissions_data)  # Use the set() method to set the many-to-many relationship

        return instance
