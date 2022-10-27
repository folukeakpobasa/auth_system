from rest_framework import serializers
from user_auth.models import CustomUser,  Role

class CustomUserSeriallizer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name')
        # extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validate_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validate_data)

    def update(self, instance, validate_data):
        """update a user, setting the password correctly and return it"""
        password = validate_data.pop('password', None)
        user = super().update(instance, validate_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class RoleSerilaizer(serializers.Serializer):
    class Meta:
        model = get_user_model()
        fields = ('user_role', 'customer_user')
    pass


class ManageUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
