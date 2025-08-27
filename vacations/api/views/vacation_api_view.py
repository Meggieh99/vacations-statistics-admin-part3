from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from typing import Any
from vacations.models import Vacation, Like, User
from vacations.api.serializers.vacation_serializer import (
    VacationSerializer, EditVacationSerializer, AddVacationSerializer
)



class VacationListView(APIView):
    """
    Returns a list of all vacations in the system,
    including like count and whether the current user liked each vacation.
    """

    def get(self, request) -> Response:
        """
        Handle GET requests to retrieve all vacations.
        Adds 'like_count' and 'liked_by_user' to each vacation.
        """
        user_id: int = request.session.get("user_id", 0)
        vacations = Vacation.objects.all().order_by('start_date')

        serialized = VacationSerializer(vacations, many=True).data

        for vacation in serialized:
            vacation_id = vacation["id"]
            vacation["like_count"] = Like.objects.filter(vacation_id=vacation_id).count()
            vacation["liked_by_user"] = Like.objects.filter(
                vacation_id=vacation_id,
                user_id=user_id
            ).exists()

        return Response(serialized)


class AddVacationView(APIView):
    """
    API endpoint to add a new vacation (Admin only).
    """

    def post(self, request) -> Response:
        """
        Handle POST request to add a vacation.
        """
        user_id = request.session.get("user_id")
        user = User.objects.filter(id=user_id).first()

        if not user or not user.is_staff:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        serializer: AddVacationSerializer = AddVacationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Vacation added successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditVacationView(APIView):
    """
    Return JSON :API endpoint to view or update a vacation (Admin only).
    """

    def get(self, request, vacation_id: int) -> Response:
        """
        Retrieve vacation data for editing.
        """
        user_id = request.session.get("user_id")
        user = User.objects.filter(id=user_id).first()

        if not user or not user.is_staff:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        try:
            vacation = Vacation.objects.get(id=vacation_id)
        except Vacation.DoesNotExist:
            return Response({"error": "Vacation not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = EditVacationSerializer(vacation)
        return Response(serializer.data)

    def put(self, request, vacation_id: int) -> Response:
        """
        Update vacation data.
        """
        user_id = request.session.get("user_id")
        user = User.objects.filter(id=user_id).first()

        if not user or not user.is_staff:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        try:
            vacation = Vacation.objects.get(id=vacation_id)
        except Vacation.DoesNotExist:
            return Response({"error": "Vacation not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = EditVacationSerializer(vacation, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Vacation updated successfully."})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteVacationView(APIView):
    """
    API endpoint to delete a vacation (Admin only).
    """

    def delete(self, request, vacation_id: int) -> Response:
        """
        Delete a vacation by ID.
        """
        user_id = request.session.get("user_id")
        user = User.objects.filter(id=user_id).first()

        if not user or not user.is_staff:
            return Response({"detail": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        deleted, _ = Vacation.objects.filter(id=vacation_id).delete()
        if deleted == 0:
            return Response({"error": "Vacation not found."}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Vacation deleted successfully."}, status=status.HTTP_200_OK)
