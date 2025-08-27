from django.shortcuts import render, redirect
from django.views import View
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.conf import settings
import os
import datetime
from vacations.services import add_vacation, get_all_countries
from vacations.models import User


class AddVacationPageView(View):
    """
    View for rendering and handling the vacation creation form.
    Accessible only by admin users (user_id = 1).
    """

    def get(self, request):
        """
        Render the Add Vacation form if the user is admin.

        :param request: Django HTTP request object
        :return: Rendered HTML page with form
        """
        if not self._is_admin(request):
            return redirect('vacation-list')

        countries = get_all_countries()
        return render(request, 'vacations/add_vacation.html', {'countries': countries})

    def post(self, request):
        """
        Process submitted vacation data and create a new vacation.

        :param request: Django HTTP request object
        :return: Redirect to admin list or re-render form with error
        """
        if not self._is_admin(request):
            return redirect('vacation-list')

        try:
            country_id: int = int(request.POST.get("country_id"))
            description: str = request.POST.get("description")
            start_date_str: str = request.POST.get("start_date")
            end_date_str: str = request.POST.get("end_date")
            price: float = float(request.POST.get("price"))

            if not all([country_id, description, start_date_str, end_date_str, price]):
                raise ValidationError("All fields are required.")

            # Convert strings to datetime.date
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
            today = datetime.date.today()

            if price < 0 or price > 10000:
                raise ValidationError("Price must be between 0 and 10,000.")
            if start_date < today or end_date < today:
                raise ValidationError("Dates cannot be in the past.")
            if end_date < start_date:
                raise ValidationError("End date cannot be before start date.")

            image = request.FILES.get("image")
            if not image:
                raise ValidationError("Image file is required.")

            # Save image file and store only filename
            image_filename = image.name
            image_path = os.path.join(settings.BASE_DIR, 'static', 'images', image_filename)
            with open(image_path, 'wb+') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            add_vacation(
                country_id=country_id,
                description=description,
                start_date=start_date,
                end_date=end_date,
                price=price,
                image_filename=image_filename
            )

            messages.success(request, "Vacation was added successfully!")
            return redirect('admin-vacation-list')

        except Exception as e:
            countries = get_all_countries()
            return render(request, 'vacations/add_vacation.html', {
                'error_message': str(e),
                'countries': countries
            })

    def _is_admin(self, request) -> bool:
        """
        Check if current session belongs to an admin user.

        :param request: Django HTTP request object
        :return: True if user is admin, False otherwise
        """
        user_id = request.session.get("user_id")
        user = User.objects.filter(id=user_id).first()
        return bool(user and user.is_staff)
