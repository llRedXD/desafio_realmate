from rest_framework import serializers

from chat_hooks.models import Conversation, direction_message


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
