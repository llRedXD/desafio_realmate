from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(
                "/conversations/view"
            )  # Altere 'home' para a URL desejada após o login.
        else:
            messages.error(request, "Usuário ou senha inválidos.")

    return render(
        request, "login.html"
    )  # Certifique-se de que o template 'login.html' existe.


def lougout_view(request):
    logout(request)
    return redirect("/login/")  # Redireciona para a página de login após o logout.
