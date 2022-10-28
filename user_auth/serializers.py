from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from user_auth.models import CustomUser,  Role, UserGroup


class CustomUserSeriallizer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=4, write_only=True, style={
                                     "input_type": "password"})

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password', 'id')


class RoleSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('user_role', 'customer_user')


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = ('user_group', 'customer_user')


class MyAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label=_("Email"))
    password = serializers.CharField(
        label=_("Password",),
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        print("attr", attrs)
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
            return user
        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=30, min_length=4, style={
                                     "input_type": "password"}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "token", "full_name"]
        read_only_fields = ["full_name", "token"]
