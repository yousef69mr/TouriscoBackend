from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import User


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
        fields = ('id', 'username', 'email', 'password', 'profile_image', 'nationality',
                  'gender', 'phone', 'is_active', 'is_staff', 'is_superuser', 'is_verified')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        instance.set_is_active(True)

        if password is not None:
            instance.set_password(password)
            instance.set_visible_password(password)
        instance.save()
        return instance
