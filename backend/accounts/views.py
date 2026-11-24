import json
from pathlib import Path
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Document
from .tasks import run_pipeline

User = get_user_model()


def _body(request):
    try:
        return json.loads(request.body)
    except ValueError:
        return {}







def as_dict(doc):
    return {"id": doc.id, "title": doc.title, "status": doc.status}


@ensure_csrf_cookie
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def documents(request):
    if request.method == "POST":
        pdf = request.FILES.get("pdf")
        if pdf is None:
            return Response({"error": "A PDF file is required."}, status=400)
        if pdf.read(5) != b"%PDF-":
            return Response({"error": "File is not a valid PDF."}, status=400)
        pdf.seek(0)
        doc = Document.objects.create(owner=request.user, pdf=pdf, title=Path(pdf.name).stem[:80])
        transaction.on_commit(lambda: run_pipeline.delay(doc.id))
        return Response(as_dict(doc), status=201)

    docs = Document.objects.filter(owner=request.user).order_by("-created_at")
    return Response([as_dict(d) for d in docs])


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def document_detail(request, pk):
    doc = get_object_or_404(Document, pk=pk, owner=request.user)
    return Response(as_dict(doc))













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



@require_POST
def login_check(request):
    data = _body(request)
    user = authenticate(
        username=str(data.get("username", "")).strip(),
        password=str(data.get("password", "")),
    )
    if user is None:
        return JsonResponse({"errors": {"form": "Invalid username or password."}}, status=401)
    auth_login(request, user)
    return JsonResponse({"id": user.id, "username": user.username})


@require_POST
def logout_view(request):
    auth_logout(request)
    return JsonResponse({"ok": True})


@require_GET
def me(request):
    if request.user.is_authenticated:
        return JsonResponse({"user": request.user.username})
    return JsonResponse({"user": None})


@require_GET
@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({"ok": True})