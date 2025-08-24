# views.py  (Django)
from __future__ import annotations
import json
from typing import Any, Dict, Iterable, List, Tuple
from django.http import HttpRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from vacations.models import Like, User, Vacation


def _json_error(message: str, status: int = 400) -> JsonResponse:
    """Return a JSON error payload with a given HTTP status code."""
    return JsonResponse({"error": message}, status=status)


def _normalize_role_name(name: str | None) -> str:
    """Normalize role names to a comparable canonical form."""
    if not name:
        return ""
    s = str(name).strip().lower()
    # Replace separators and collapse whitespace
    s = s.replace("-", " ").replace("_", " ")
    s = " ".join(s.split())
    return s


def _is_admin_user(user: User) -> bool:
    """Return True if the user's role represents an admin."""
    role_name = _normalize_role_name(getattr(getattr(user, "role", None), "name", None))
    if not role_name:
        return False
    # Accept common variations, but keep the original contract: startswith("admin")
    if role_name.startswith("admin"):
        return True
    return role_name in {"administrator", "super admin", "superadmin", "admin user"}


def _require_admin_session(request: HttpRequest) -> Tuple[bool, JsonResponse | None]:
    """Validate that the request has an authenticated admin session."""
    user_id: int | None = request.session.get("user_id")
    if not user_id:
        return False, _json_error("Unauthorized", status=401)

    try:
        user: User = User.objects.select_related("role").get(pk=user_id)
    except User.DoesNotExist:
        return False, _json_error("Unauthorized", status=401)

    if not _is_admin_user(user):
        return False, _json_error("Forbidden: admin only", status=403)

    return True, None


@csrf_exempt
@require_POST
def login_view(request: HttpRequest) -> JsonResponse:
    """Login endpoint for the stats area (admin only, session-based)."""
    try:
        body: Dict[str, Any] = json.loads(request.body.decode("utf-8"))
    except Exception:
        return _json_error("Invalid JSON body")

    email: str = str(body.get("email", "")).strip().lower()
    password: str = str(body.get("password", "")).strip()

    if not email or not password:
        return _json_error("Missing credentials", status=401)

    try:
        user: User = User.objects.select_related("role").get(email=email)
    except User.DoesNotExist:
        return _json_error("Invalid credentials", status=401)

    # NOTE: Plain-text password per the course skeleton
    if user.password != password:
        return _json_error("Invalid credentials", status=401)

    if not _is_admin_user(user):
        # Dev-friendly trace (safe to leave, but remove if you prefer quieter logs)
        print(f"[login] non-admin login attempt: email={user.email!r}, role={getattr(getattr(user, 'role', None), 'name', None)!r}")
        return _json_error("Forbidden: admin only", status=403)

    request.session["user_id"] = user.id
    return JsonResponse({"success": True})


@csrf_exempt
@require_POST
def logout_view(request: HttpRequest) -> JsonResponse:
    """
    Logout endpoint that clears the current session.
    """
    request.session.flush()
    response = JsonResponse({"success": True})
    response.delete_cookie("sessionid")
    return response

@require_GET
def vacations_stats(request: HttpRequest) -> JsonResponse:
    """Return counts of past/ongoing/future vacations (admin session required)."""
    ok, err = _require_admin_session(request)
    if not ok:
        return err  # type: ignore[return-value]

    from django.utils import timezone
    now = timezone.now().date()

    past: int = Vacation.objects.filter(end_date__lt=now).count()
    ongoing: int = Vacation.objects.filter(start_date__lte=now, end_date__gte=now).count()
    future: int = Vacation.objects.filter(start_date__gt=now).count()
    return JsonResponse(
        {"pastVacations": past, "ongoingVacations": ongoing, "futureVacations": future}
    )


@require_GET
def total_users(request: HttpRequest) -> JsonResponse:
    """Return total number of users (admin session required)."""
    ok, err = _require_admin_session(request)
    if not ok:
        return err  # type: ignore[return-value]

    total: int = User.objects.count()
    return JsonResponse({"totalUsers": total})


@require_GET
def total_likes(request: HttpRequest) -> JsonResponse:
    """Return total number of likes (admin session required)."""
    ok, err = _require_admin_session(request)
    if not ok:
        return err  # type: ignore[return-value]

    total: int = Like.objects.count()
    return JsonResponse({"totalLikes": total})


@require_GET
def likes_distribution(request: HttpRequest) -> JsonResponse:
    """Return likes distribution per destination (admin session required)."""
    ok, err = _require_admin_session(request)
    if not ok:
        return err  # type: ignore[return-value]

    from django.db.models import Count

    rows: Iterable[Dict[str, Any]] = (
        Like.objects
        .values("vacation__country__name")
        .annotate(likes=Count("id"))
        .order_by("vacation__country__name")
    )

    data: List[Dict[str, Any]] = []
    for r in rows:
        country_name: str = str(r.get("vacation__country__name") or "")
        data.append({"destination": country_name, "likes": int(r["likes"])})
    return JsonResponse(data, safe=False)

@require_GET
def session_view(request: HttpRequest) -> JsonResponse:
    """Return session authentication status for frontend use."""
    user_id: int | None = request.session.get("user_id")
    return JsonResponse({"authenticated": bool(user_id)})
