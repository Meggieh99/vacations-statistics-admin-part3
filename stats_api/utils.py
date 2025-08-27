"""Part III – Admin validation helper."""

from typing import Optional
from django.http import HttpRequest
from stats_api.models import User, Vacation, Like



def get_logged_in_admin(request: HttpRequest) -> Optional[User]:
    """
    Returns the currently logged-in admin user or None.
    Requires session['user_id'] and the user's role name to be 'ADMIN'.
    """
    user_id = request.session.get("user_id")
    if user_id is None:
        return None

    try:
        user = User.objects.select_related("role").get(id=user_id)
    except User.DoesNotExist:
        return None

    role_name = (user.role.name or "").upper()
    return user if role_name == "ADMIN" else None
