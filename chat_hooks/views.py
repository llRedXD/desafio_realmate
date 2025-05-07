from django.shortcuts import render


def view_conversations(request):
    return render(request, "conversations.html")


def view_conversation(request, conversation_id):
    return render(
        request, "conversation_detail.html", {"conversation_id": conversation_id}
    )
