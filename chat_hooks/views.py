from django.shortcuts import render


def view_conversations(request):
    if not request.user.is_authenticated:
        return render(request, "login.html")
    return render(request, "conversations.html")
