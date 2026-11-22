import json

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

User = get_user_model()


def _body(request):
    try:
        return json.loads(request.body)
    except ValueError:
        return {}


@csrf_exempt  # temporary: removed when we add sessions/tokens
@require_POST
def register(request):
    data = _body(request)
    username = str(data.get("username", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    errors = {}

    if not username:
        errors["username"] = "Username is required."
    elif User.objects.filter(username__iexact=username).exists():
        errors["username"] = "That username is taken."

    if "@" not in email:
        errors["email"] = "Enter a valid email."
    elif User.objects.filter(email__iexact=email).exists():
        errors["email"] = "That email is already registered."

    if not password:
        errors["password"] = "Password is required."
    else:
        try:
            validate_password(password, user=User(username=username, email=email))
        except ValidationError as e:
            errors["password"] = " ".join(e.messages)

    if errors:
        return JsonResponse({"errors": errors}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    return JsonResponse({"id": user.id, "username": user.username}, status=201)


@csrf_exempt  # temporary
@require_POST
def login_check(request):
    data = _body(request)
    user = authenticate(
        username=str(data.get("username", "")).strip(),
        password=str(data.get("password", "")),
    )
    if user is None:
        return JsonResponse({"errors": {"form": "Invalid username or password."}}, status=401)
    return JsonResponse({"id": user.id, "username": user.username})