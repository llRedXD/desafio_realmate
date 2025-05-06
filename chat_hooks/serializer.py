from rest_framework import serializers
from chat_hooks.models import Conversation, Message


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for ChatHook model.
    """

    class Meta:
        model = Conversation
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for ChatHookMessage model.
    """

    class Meta:
        model = Message
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
