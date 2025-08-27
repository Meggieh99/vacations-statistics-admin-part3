from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views import View
from django.http import HttpRequest, HttpResponse
from vacations.models import User
from vacations.api.serializers.user_serializer import RegisterSerializer


class RegisterPageView(View):
    """
    Handle user registration via HTML form.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        """Render the registration form."""
        return render(request, 'auth/register.html')

    def post(self, request: HttpRequest) -> HttpResponse:
        """Process registration form data."""
        serializer = RegisterSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.save()
            request.session['user_id'] = user.id
            return redirect(reverse('vacation-list'))

        for field, errors in serializer.errors.items():
            for error in errors:
                messages.error(request, f"{field}: {error}")
        return render(request, 'auth/register.html')
