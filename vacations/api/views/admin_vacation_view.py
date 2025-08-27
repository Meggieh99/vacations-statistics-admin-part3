from django.views import View
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from vacations.models import User, Vacation
from vacations.api.serializers.vacation_serializer import EditVacationSerializer


class AdminVacationListView(View):
    """
    View for displaying vacations to Admin users only.
    """

    def get(self, request: HttpRequest) -> HttpResponse:
        user_id = request.session.get('user_id')

        if not user_id:
            return redirect(reverse('login-form'))

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return redirect(reverse('login-form'))

        # check if user is admin
        if user.role.name.lower() != 'admin':
            return HttpResponse("Unauthorized", status=403)

        # get all vacations
        vacations = Vacation.objects.all().order_by('start_date')

        context = {
            'vacations': vacations,
            'user': user
        }

        return render(request, 'vacations/admin_vacation_list.html', context)
    
