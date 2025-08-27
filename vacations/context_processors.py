from vacations.models import User

def current_user_full_name(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return {}

    user = User.objects.filter(id=user_id).first()
    if not user:
        return {}

    return {
        "current_user_full_name": f"{user.first_name} {user.last_name}"
    }
