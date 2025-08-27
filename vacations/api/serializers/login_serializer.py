from typing import Optional, Any
from rest_framework import serializers
from vacations.models import User


class LoginSerializer(serializers.Serializer):
    """
    Serializer for login validation. Ensures password has at least 8 characters.
    """

    email: serializers.EmailField = serializers.EmailField()
    password: serializers.CharField = serializers.CharField(
        min_length=8, 
        error_messages={"min_length": "Password must be at least 8 characters."}
    )

    def validate(self, data: dict[str, Any]) -> dict[str, Any]:
        """
        Validate email and password against database.
        Raises error if credentials are invalid.
        """
        email: str = data.get('email')
        password: str = data.get('password')

        user: Optional[User] = User.objects.filter(email=email, password=password).first()
        if user is None:
            raise serializers.ValidationError("Invalid email or password")

        data['user'] = user
        return data
