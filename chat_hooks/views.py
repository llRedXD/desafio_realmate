from django.shortcuts import render


def view_conversation(request):
    return render(request, "conversations.html")
