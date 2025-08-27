from rest_framework import serializers
from vacations.models import User, Role

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new user.
    Validates password length and unique email.
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def validate_password(self, value: str) -> str:
        """
        Validate password length.

        :param value: Password as a string
        :raises serializers.ValidationError: If password is less than 8 characters long
        :return: Validated password
        """
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def create(self, validated_data: dict) -> User:
        user_role: Role = Role.objects.get(name='user')
        return User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=user_role
        )
