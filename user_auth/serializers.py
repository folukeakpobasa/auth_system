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
        fields = ('email', 'first_name', 'last_name', 'password')


class RoleSerilaizer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('user_role', 'customer_user')


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = ('user_group', 'customer_user')
