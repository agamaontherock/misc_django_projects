from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("chat_app:chat_room", room_id=1)  # зміни на свій URL
        else:
            messages.error(request, "Невірний логін або пароль")

    return render(request, "chat_app/login_page.html")


@login_required
def logout_view(request):
    logout(request)
    return redirect("chat_app:login")


def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Паролі не співпадають")
            return redirect("chat_app:register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Користувач вже існує")
            return redirect("chat_app:register")

        User.objects.create_user(username=username, password=password1)
        return redirect("chat_app:login")

    return render(request, "chat_app/register_page.html")


@login_required
def chat_room(request, room_id):
    return render(request, "chat_app/chat_room.html", {"room_id": room_id})
