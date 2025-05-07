from rest_framework import serializers

from chat_hooks.models import Conversation, direction_message


# Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for ChatHook model.
    """

    class Meta:
        model = Conversation
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class MessageSerializer(serializers.Serializer):
    """
    Serializer for Message model.
    """

    id = serializers.UUIDField(read_only=True)
    direction = serializers.ChoiceField(choices=direction_message.choices)
    content = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)


class ConversationIdSerializer(serializers.ModelSerializer):
    """
    Serializer for one conversation.
    """

    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ["id", "messages", "status", "created_at", "updated_at"]


# Webhook Serializer
class NewConversationSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)


class NewMessageSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)
    direction = serializers.ChoiceField(choices=["SENT", "RECEIVED"], required=True)
    content = serializers.CharField(required=True)
    conversation_id = serializers.UUIDField(required=True)


class CloseConversationSerializer(serializers.Serializer):
    id = serializers.UUIDField(required=True)


class WebhookSerializer(serializers.Serializer):
    type = serializers.ChoiceField(
        choices=["NEW_CONVERSATION", "NEW_MESSAGE", "CLOSE_CONVERSATION"], required=True
    )
    timestamp = serializers.DateTimeField(required=True)
    data = serializers.JSONField(required=True)

    def validate(self, attrs):
        event_type = attrs.get("type")
        data = attrs.get("data")

        if event_type == "NEW_CONVERSATION":
            serializer = NewConversationSerializer(data=data)
        elif event_type == "NEW_MESSAGE":
            serializer = NewMessageSerializer(data=data)
        elif event_type == "CLOSE_CONVERSATION":
            serializer = CloseConversationSerializer(data=data)
        else:
            raise serializers.ValidationError("Tipo de evento inválido")

        serializer.is_valid(raise_exception=True)
        attrs["data"] = serializer.validated_data
        return attrs
