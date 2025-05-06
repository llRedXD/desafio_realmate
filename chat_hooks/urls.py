from django.urls import path
from chat_hooks.views import ConversationViewSet, WebhookViewSet

urlpatterns = [
    path(
        "conversations/",
        ConversationViewSet.as_view({"get": "list"}),
        name="conversation-list",
    ),
    path(
        "webhook/",
        WebhookViewSet.as_view({"post": "create"}),
        name="webhook",
    ),
]
