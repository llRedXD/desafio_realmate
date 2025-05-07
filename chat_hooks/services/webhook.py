from rest_framework import status
from rest_framework.response import Response
from chat_hooks.models import Conversation, Message


def create_conversation(data):
    conversation_id = data.get("id")
    if not conversation_id:
        return Response(
            {"error": "ID da conversa não informado"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    # Cria conversa com estado OPEN
    conversation, created = Conversation.objects.get_or_create(
        id=conversation_id, defaults={"state": "OPEN"}
    )
    if not created:
        return Response(
            {"error": "Conversation já existe"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    return Response({"message": "Conversation criada"}, status=status.HTTP_201_CREATED)


def close_conversation(data):
    conversation_id = data.get("id")
    if not conversation_id:
        return Response(
            {"error": "ID da conversa não informado"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    try:
        conversation = Conversation.objects.get(id=conversation_id)
    except Conversation.DoesNotExist:
        return Response(
            {"error": "Conversation não encontrada"},
            status=status.HTTP_404_NOT_FOUND,
        )
    conversation.status = "CLOSED"
    conversation.save()
    return Response({"message": "Conversation fechada"}, status=status.HTTP_200_OK)


def new_message(data):
    message_id = data.get("id")
    direction = data.get("direction")
    content = data.get("content")
    conversation_id = data.get("conversation_id")

    if not all([message_id, direction, content, conversation_id]):
        return Response(
            {"error": "Dados insuficientes para criar mensagem"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        conversation = Conversation.objects.get(id=conversation_id)
    except Conversation.DoesNotExist:
        return Response(
            {"error": "Conversation não encontrada"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if conversation.status == "CLOSED":
        return Response(
            {"error": "Não é possível adicionar mensagem a conversa fechada"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if direction not in ["SENT", "RECEIVED"]:
        return Response(
            {"error": "Direção inválida"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    message, created = Message.objects.get_or_create(
        id=message_id,
        defaults={
            "direction": direction,
            "content": content,
            "conversation": conversation,
        },
    )
    if not created:
        return Response(
            {"error": "Message já existe"}, status=status.HTTP_400_BAD_REQUEST
        )
    return Response({"message": "Message criada"}, status=status.HTTP_201_CREATED)
