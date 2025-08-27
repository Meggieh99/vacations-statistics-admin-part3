from typing import Optional, List
from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from vacations.models import Vacation, Country, User
from vacations.services import update_vacation


class EditVacationPageView(View):
    """
    Handles the editing of an existing vacation by admin users.
    Shows the form without pre-filled values, enforcing required inputs.
    """

    def get(self, request, vacation_id: int):
        """
        Displays the edit vacation form. Access is allowed for admin users only.

        :param request: HTTP request object
        :param vacation_id: ID of the vacation to edit
        :return: Rendered HTML page with edit form
        """
        user_id: Optional[int] = request.session.get("user_id")
        user: Optional[User] = User.objects.filter(id=user_id).first()

        if not user or not user.is_staff:
            return redirect("login-form")

        vacation = get_object_or_404(Vacation, id=vacation_id)
        countries = Country.objects.all()

        return render(request, "vacations/edit_vacation.html", {
            "vacation": vacation,
            "countries": countries,
        })

    def post(self, request, vacation_id: int):
        """
        Processes the submitted edit vacation form.
        Validates the data and updates the vacation.

        :param request: HTTP request with form data
        :param vacation_id: ID of the vacation being edited
        :return: Redirect to admin list or render form with errors
        """
        user_id: Optional[int] = request.session.get("user_id")
        user: Optional[User] = User.objects.filter(id=user_id).first()

        if not user or not user.is_staff:
            return redirect("login-form")

        vacation = get_object_or_404(Vacation, id=vacation_id)

        # Extract fields from form
        country_id = request.POST.get("country_id")
        description = request.POST.get("description", "").strip()
        start_date = request.POST.get("start_date", "").strip()
        end_date = request.POST.get("end_date", "").strip()
        price = request.POST.get("price", "").strip()
        image = request.FILES.get("image")
        image_filename = image.name if image else ""

        # Validate required fields
        errors: List[str] = []
        if not country_id:
            errors.append("Country is required.")
        if not description:
            errors.append("Description is required.")
        if not start_date:
            errors.append("Start date is required.")
        if not end_date:
            errors.append("End date is required.")
        if not price:
            errors.append("Price is required.")

        if errors:
            countries = Country.objects.all()
            return render(request, "vacations/edit_vacation.html", {
                "vacation": vacation,
                "countries": countries,
                "errors": errors,
            })

        # Update the country manually, since update_vacation does not handle it
        vacation.country = Country.objects.get(id=int(country_id))

        # Try to update the rest of the fields
        try:
            update_vacation(
                vacation_id=vacation.id,
                description=description,
                start_date=start_date,
                end_date=end_date,
                price=float(price),
                image_filename=image_filename,
            )
        except ValidationError as ve:
            countries = Country.objects.all()
            return render(request, "vacations/edit_vacation.html", {
                "vacation": vacation,
                "countries": countries,
                "errors": ve.messages,
            })

        return redirect("admin-vacation-list")
