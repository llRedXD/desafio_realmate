from django.db import models


# Create your models here.
class BaseModel(models.Model):
    """
    Base model with common fields.
    """

    created_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created_by",
    )
    updated_by = models.ForeignKey(
        "auth.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated_by",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class conversation_state(models.TextChoices):
    """
    Enum for states choices.
    """

    OPEN = "open", "Open"
    CLOSED = "closed", "Closed"


class Conversation(BaseModel):
    """
    Model to store conversation data.
    """

    id = models.UUIDField(primary_key=True, editable=False)
    state = models.CharField(
        max_length=10,
        choices=conversation_state.choices,
        default=conversation_state.OPEN,
    )

    def __str__(self):
        return f"Conversation {self.id} for user {self.user_id}"


class direction_message(models.TextChoices):
    """
    Enum for message direction choices.
    """

    SENT = "sent", "Sent"
    RECEIVED = "received", "Received"


class Message(BaseModel):
    """
    Model to store message data.
    """

    id = models.UUIDField(primary_key=True, editable=False)
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    direction_message = models.CharField(
        max_length=10,
        choices=direction_message.choices,
        null=True,
        blank=True,
    )
    content = models.TextField()

    def __str__(self):
        return f"Message {self.id} from {self.sender} in conversation {self.conversation.id}"
