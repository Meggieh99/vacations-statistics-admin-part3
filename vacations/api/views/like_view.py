from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from vacations.models import Like, Vacation

class LikeVacationView(APIView):
    """
    Add a like for a vacation by the authenticated user (via session).
    """

    def post(self, request, vacation_id: int) -> Response:
        user_id = request.session.get("user_id")

        if not user_id:
            return Response({"error": "User not authenticated"}, status=status.HTTP_403_FORBIDDEN)

        if not Vacation.objects.filter(id=vacation_id).exists():
            return Response({"error": "Vacation not found"}, status=status.HTTP_404_NOT_FOUND)

        if Like.objects.filter(user_id=user_id, vacation_id=vacation_id).exists():
            return Response({"error": "Already liked"}, status=status.HTTP_400_BAD_REQUEST)

        Like.objects.create(user_id=user_id, vacation_id=vacation_id)
        return Response({"message": "Like added successfully"}, status=status.HTTP_201_CREATED)


class UnlikeVacationView(APIView):
    """
    Remove a like for a vacation by the authenticated user (via session).
    """

    def post(self, request, vacation_id: int) -> Response:
        user_id = request.session.get("user_id")

        if not user_id:
            return Response({"error": "User not authenticated"}, status=status.HTTP_403_FORBIDDEN)

        deleted, _ = Like.objects.filter(user_id=user_id, vacation_id=vacation_id).delete()

        if deleted == 0:
            return Response({"error": "Like not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "Like removed successfully"})
