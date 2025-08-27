from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from vacations.models import Vacation, Like



class VacationListPageView(TemplateView):
    """
    Render vacation list page. Accessible to all users.
    If logged in, will show which vacations the user liked.
    """

    template_name = 'vacations/vacation_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.session.get('user_id')  # might be None

        vacations = Vacation.objects.all().order_by('start_date')

        vacation_data = []
        for vacation in vacations:
            liked = False
            if user_id:
                liked = Like.objects.filter(vacation_id=vacation.id, user_id=user_id).exists()

            vacation_data.append({
                'id': vacation.id,
                'country': vacation.country.name,
                'description': vacation.description,
                'start_date': vacation.start_date,
                'end_date': vacation.end_date,
                'price': vacation.price,
                'image_filename': vacation.image_filename,
                'like_count': Like.objects.filter(vacation_id=vacation.id).count(),
                'liked_by_user': liked,
            })

        context['vacations'] = vacation_data
        return context
