from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token


User = get_user_model().objects.create_user


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'bio', 'profile_picture']
        read_only_fields = ['id']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField()
    password2 = serializers.CharField(write_only=True, required=True)


class Meta:
    model = User
    fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', 'bio']


def validate(self, attrs):
    if attrs.get('password') != attrs.get('password2'):
        raise serializers.ValidationError({'password': "Password fields didn't match."})
        # optional: validate password strength
    validate_password(attrs.get('password'))
    return attrs


def create(self, validated_data):
    validated_data.pop('password2', None)
    password = validated_data.pop('password')
    user = User(**validated_data)
    user.set_password(password)
    user.save()
    # create token
    Token.objects.create(user=user)
    return user