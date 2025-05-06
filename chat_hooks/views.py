from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from chat_hooks.models import Conversation, Message
from chat_hooks.serializer import MessageSerializer, ConversationSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Conversation model.
    """

    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        List all Conversation.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Message model.
    """

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        List all Messages.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class WebhookViewSet(viewsets.ViewSet):
    """
    ViewSet for handling webhooks.
    """

    def create(self, request):
        payload = request.data
        event_type = payload.get("type")
        data = payload.get("data", {})

        if not event_type or not data:
            return Response(
                {"error": "Payload inválido"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Processa evento de nova conversa
        if event_type == "NEW_CONVERSATION":
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
            return Response(
                {"message": "Conversation criada"}, status=status.HTTP_201_CREATED
            )

        # Processa evento de nova mensagem
        elif event_type == "NEW_MESSAGE":
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

            if conversation.state == "CLOSED":
                return Response(
                    {"error": "Não é possível adicionar mensagem a conversa fechada"},
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
            return Response(
                {"message": "Message criada"}, status=status.HTTP_201_CREATED
            )

        # Processa evento de fechar conversa
        elif event_type == "CLOSE_CONVERSATION":
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
            conversation.state = "CLOSED"
            conversation.save()
            return Response(
                {"message": "Conversation fechada"}, status=status.HTTP_200_OK
            )

        else:
            return Response(
                {"error": "Tipo de evento inválido"}, status=status.HTTP_400_BAD_REQUEST
            )
