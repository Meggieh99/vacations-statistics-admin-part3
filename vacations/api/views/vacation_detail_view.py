from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.contrib import messages
from vacations.models import Vacation


class VacationDetailView(View):
    """
    Display full vacation details. Requires user to be logged in.
    If not logged in, render the login form with an error message (no redirect).
    """

    def get(self, request, vacation_id: int):
        user_id = request.session.get("user_id")

        if not user_id:
            return render(request, "auth/login.html")

        vacation = get_object_or_404(Vacation, id=vacation_id)
        return render(request, "vacations/vacation_detail.html", {"vacation": vacation})
