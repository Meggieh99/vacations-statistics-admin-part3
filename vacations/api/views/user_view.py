from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from typing import Any
from vacations.api.serializers.user_serializer import RegisterSerializer
from vacations.api.serializers.login_serializer import LoginSerializer



class RegisterView(APIView):
    """
    API endpoint for registering a new user.
    """

    def post(self, request: Any) -> Response:
        """
        Handle POST request to register a user.
        """
        serializer: RegisterSerializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    API endpoint for user login.
    """

    def post(self, request: Any) -> Response:
        """
        Handle POST request to authenticate a user.
        """
        serializer: LoginSerializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response({
                "message": "Login successful",
                "user_id": user.id,
                "email": user.email,
                "full_name": f"{user.first_name} {user.last_name}",
                "role": user.role.name,
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
