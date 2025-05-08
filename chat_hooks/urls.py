from django.urls import path
from chat_hooks.api.webhook import WebhookViewSet
from chat_hooks.api.conversation import ConversationViewSet
from chat_hooks.views import view_conversation, view_conversations

urlpatterns = [
    path(
        "conversations/",
        ConversationViewSet.as_view({"get": "list"}),
        name="conversation-list",
    ),
    path(
        "conversations/<uuid:pk>/",
        ConversationViewSet.as_view({"get": "retrieve"}),
        name="conversation-detail",
    ),
    path(
        "webhook/",
        WebhookViewSet.as_view({"post": "create"}),
        name="webhook",
    ),
    path(
        "conversations/view/",
        view_conversations,
        name="view-conversation",
    ),
    path(
        "conversations/view/<uuid:conversation_id>/",
        view_conversation,
        name="view-conversation-detail",
    ),
]
