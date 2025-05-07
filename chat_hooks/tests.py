from django.test import TestCase, Client

from chat_hooks.models import Conversation, Message

# Create your tests here.


class ConversationTestCase(TestCase):
    """
    Test case for Conversation model.
    """

    def setUp(self):
        """
        Set up test data.
        """
        # Create a conversation instance
        self.conversation = Conversation.objects.create(
            id="123e4567-e89b-12d3-a456-426614174000",
        )

    def test_conversation_creation(self):
        """
        Test conversation creation.
        """
        self.assertIsInstance(self.conversation, Conversation)
        self.assertEqual(self.conversation.status, "open")

    def test_conversation_str(self):
        """
        Test string representation of conversation.
        """
        self.assertEqual(
            str(self.conversation), "Conversation 123e4567-e89b-12d3-a456-426614174000"
        )


class MessageTestCase(TestCase):
    """
    Test case for Message model.
    """

    def setUp(self):
        """
        Set up test data.
        """
        # Create a conversation instance
        self.conversation = Conversation.objects.create(
            id="123e4567-e89b-12d3-a456-426614174000",
        )

    def test_message_sent_creation(self):
        """
        Test message sentcreation.
        """
        # Create a message instance
        message = self.conversation.messages.create(
            id="123e4567-e89b-12d3-a456-426614174001",
            direction="sent",
            content="Hello, world!",
        )

        self.assertIsInstance(message, Message)
        self.assertEqual(message.direction, "sent")
        self.assertEqual(message.content, "Hello, world!")

    def test_message_received_creation(self):
        """
        Test message received creation.
        """
        # Create a message instance
        message = self.conversation.messages.create(
            id="123e4567-e89b-12d3-a456-426614174002",
            direction="received",
            content="Hello, world!",
        )

        self.assertIsInstance(message, Message)
        self.assertEqual(message.direction, "received")
        self.assertEqual(message.content, "Hello, world!")

    def test_message_str(self):
        """
        Test string representation of message.
        """
        message = self.conversation.messages.create(
            id="123e4567-e89b-12d3-a456-426614174003",
            direction="sent",
            content="Hello, world!",
        )
        self.assertEqual(
            str(message),
            "Message 123e4567-e89b-12d3-a456-426614174003 from sent in conversation 123e4567-e89b-12d3-a456-426614174000",
        )


class WebhookApiTestCase(TestCase):
    """
    Test case for Webhook API.
    """

    def setUp(self):
        """
        Set up test data.
        """
        self.client = Client()

    def test_create_conversation(self):
        """
        Test creating a new conversation.
        """
        response = self.client.post(
            "/webhook/",
            {
                "type": "NEW_CONVERSATION",
                "timestamp": "2023-10-01T12:00:00Z",
                "data": {"id": "123e4567-e89b-12d3-a456-426614174000"},
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"], "Conversation criada")

    def test_create_conversation_invalid(self):
        """
        Test creating a new conversation with invalid data.
        """
        response = self.client.post(
            "/webhook/",
            {
                "type": "NEW_CONVERSATION",
                "timestamp": "2023-10-01T12:00:00Z",
                "data": {},
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Payload inválido")

    def test_create_convesation_id_invalid(self):
        """
        Test creating a new conversation with invalid data.
        """
        response = self.client.post(
            "/webhook/",
            {
                "type": "NEW_CONVERSATION",
                "timestamp": "2023-10-01T12:00:00Z",
                "data": {"id": ""},
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "ID da conversa não informado")
        response = self.client.post(
            "/webhook/",
            {
                "type": "NEW_CONVERSATION",
                "timestamp": "2023-10-01T12:00:00Z",
                "data": {"id": "123e4567-e89b-12d3-a456-"},
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["error"],
            "['“123e4567-e89b-12d3-a456-” is not a valid UUID.']",
        )

    def test_create_message_sent(self):
        """
        Test creating a new message.
        """
        # First, create a conversation
        self.client.post(
            "/webhook/",
            {
                "type": "NEW_CONVERSATION",
                "timestamp": "2023-10-01T12:00:00Z",
                "data": {"id": "123e4567-e89b-12d3-a456-426614174000"},
            },
            content_type="application/json",
        )

        response = self.client.post(
            "/webhook/",
            {
                "type": "NEW_MESSAGE",
                "timestamp": "2023-10-01T12:00:00Z",
                "data": {
                    "id": "123e4567-e89b-12d3-a456-426614174001",
                    "direction": "SENT",
                    "content": "Hello, world!",
                    "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
                },
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"], "Message criada")

    def test_create_message_received(self):
        """
        Test creating a new message.
        """
        # First, create a conversation
        self.client.post(
            "/webhook/",
            {
                "type": "NEW_CONVERSATION",
                "timestamp": "2023-10-01T12:00:00Z",
                "data": {"id": "123e4567-e89b-12d3-a456-426614174000"},
            },
            content_type="application/json",
        )

        response = self.client.post(
            "/webhook/",
            {
                "type": "NEW_MESSAGE",
                "timestamp": "2023-10-01T12:00:00Z",
                "data": {
                    "id": "123e4567-e89b-12d3-a456-426614174001",
                    "direction": "RECEIVED",
                    "content": "Hello, world!",
                    "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
                },
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["message"], "Message criada")

    def test_create_message_invalid(self):
        """
        Test creating a new message with invalid data.
        """
        # First, create a conversation
        self.client.post(
            "/webhook/",
            {
                "type": "NEW_CONVERSATION",
                "timestamp": "2023-10-01T12:00:00Z",
                "data": {"id": "123e4567-e89b-12d3-a456-426614174000"},
            },
            content_type="application/json",
        )

        response = self.client.post(
            "/webhook/",
            {
                "type": "NEW_MESSAGE",
                "timestamp": "2023-10-01T12:00:00Z",
                "data": {
                    "id": "",
                    "direction": "",
                    "content": "",
                    "conversation_id": "",
                },
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["error"], "Dados insuficientes para criar mensagem"
        )

    def test_create_message_conversation_not_found(self):
        """
        Test creating a new message with conversation not found.
        """
        response = self.client.post(
            "/webhook/",
            {
                "type": "NEW_MESSAGE",
                "timestamp": "2023-10-01T12:00:00Z",
                "data": {
                    "id": "123e4567-e89b-12d3-a456-426614174001",
                    "direction": "SENT",
                    "content": "Hello, world!",
                    "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
                },
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data["error"], "Conversation não encontrada")

    def test_close_conversation(self):
        """
        Test closing a conversation.
        """
        # First, create a conversation
        self.client.post(
            "/webhook/",
            {
                "type": "NEW_CONVERSATION",
                "timestamp": "2023-10-01T12:00:00Z",
                "data": {"id": "123e4567-e89b-12d3-a456-426614174000"},
            },
            content_type="application/json",
        )

        response = self.client.post(
            "/webhook/",
            {
                "type": "CLOSE_CONVERSATION",
                "timestamp": "2023-10-01T12:00:00Z",
                "data": {"id": "123e4567-e89b-12d3-a456-426614174000"},
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Conversation fechada")

    def test_create_message_conversation_closed(self):
        """
        Test creating a new message with conversation closed.
        """
        # First, create a conversation
        self.client.post(
            "/webhook/",
            {
                "type": "NEW_CONVERSATION",
                "timestamp": "2023-10-01T12:00:00Z",
                "data": {"id": "123e4567-e89b-12d3-a456-426614174000"},
            },
            content_type="application/json",
        )

        # Close the conversation
        self.client.post(
            "/webhook/",
            {
                "type": "CLOSE_CONVERSATION",
                "timestamp": "2023-10-01T12:00:00Z",
                "data": {"id": "123e4567-e89b-12d3-a456-426614174000"},
            },
            content_type="application/json",
        )

        response = self.client.post(
            "/webhook/",
            {
                "type": "NEW_MESSAGE",
                "timestamp": "2023-10-01T12:00:00Z",
                "data": {
                    "id": "123e4567-e89b-12d3-a456-426614174001",
                    "direction": "SENT",
                    "content": "Hello, world!",
                    "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
                },
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data["error"],
            "Não é possível adicionar mensagem a conversa fechada",
        )
