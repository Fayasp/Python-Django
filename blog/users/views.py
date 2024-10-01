import json
from pprint import pprint

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render

from .serializers import RegisterUserSerializer, LoginUserSerializer

# from .serializers import RegisterUser


def user(request):
    return render(request, "users/user.html")


def register_user(request: HttpRequest):
    if request.method == "POST":
        payload: dict = json.loads(request.body)
        serializer = RegisterUserSerializer(data=payload)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    return render(request, "users/user_register.html", {})


def login_user(request):
    if request.user.is_authenticated:
        return redirect("posts:list")
    if request.method == "POST":
        payload: dict = json.loads(request.body)
        serializer = LoginUserSerializer(data=payload)

        if serializer.is_valid():
            data = serializer.data
            username = data["username"]
            password = data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return JsonResponse({})
            return JsonResponse({"detail": "invalid credential"}, status=401)
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})


def logout_user(request):
    if request.method == "POST":
        logout(request)
        return redirect("home")

    return render(request, "users/logout.html")
