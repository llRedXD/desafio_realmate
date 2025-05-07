from rest_framework import viewsets, status
from rest_framework.response import Response
from chat_hooks.services.webhook import (
    close_conversation,
    create_conversation,
    new_message,
)
from chat_hooks.serializer import WebhookSerializer


class WebhookViewSet(viewsets.ViewSet):
    """
    ViewSet for handling webhooks.
    """

    serializer_class = WebhookSerializer

    def create(self, request):
        try:
            payload = request.data
            event_type = payload.get("type")
            data = payload.get("data", {})

            if not event_type or not data:
                return Response(
                    {"error": "Payload inválido"}, status=status.HTTP_400_BAD_REQUEST
                )

            # Processa evento de nova conversa
            if event_type == "NEW_CONVERSATION":
                response = create_conversation(data)
                return response

            # Processa evento de nova mensagem
            elif event_type == "NEW_MESSAGE":
                response = new_message(data)
                return response

            # Processa evento de fechar conversa
            elif event_type == "CLOSE_CONVERSATION":
                response = close_conversation(data)
                return response

            else:
                return Response(
                    {"error": "Tipo de evento inválido"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
