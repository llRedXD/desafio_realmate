import time
import uuid
import random
import datetime
import requests

# URL do endpoint de webhook
WEBHOOK_URL = "http://localhost:8000/webhook/"

# Lista para controlar conversas abertas
open_conversations = []


def get_timestamp():
    return datetime.datetime.utcnow().isoformat()


while True:
    # Escolhe aleatoriamente o tipo de evento
    event_type = random.choice(
        [
            "NEW_CONVERSATION",
            "NEW_MESSAGE",
            "NEW_MESSAGE",
            "NEW_MESSAGE",
            "NEW_MESSAGE",
            "NEW_MESSAGE",
            "CLOSE_CONVERSATION",
        ]
    )

    if event_type == "NEW_CONVERSATION":
        conv_id = str(uuid.uuid4())
        payload = {
            "type": "NEW_CONVERSATION",
            "timestamp": get_timestamp(),
            "data": {"id": conv_id},
        }
        open_conversations.append(conv_id)
    elif event_type == "NEW_MESSAGE":
        # Se não houver conversas abertas, cria uma nova
        if not open_conversations:
            conv_id = str(uuid.uuid4())
            payload = {
                "type": "NEW_CONVERSATION",
                "timestamp": get_timestamp(),
                "data": {"id": conv_id},
            }
            open_conversations.append(conv_id)
        else:
            conv_id = random.choice(open_conversations)
            direction = random.choice(["SENT", "RECEIVED"])
            payload = {
                "type": "NEW_MESSAGE",
                "timestamp": get_timestamp(),
                "data": {
                    "id": str(uuid.uuid4()),
                    "direction": direction,
                    "content": "Mensagem de teste",
                    "conversation_id": conv_id,
                },
            }
    elif event_type == "CLOSE_CONVERSATION":
        if not open_conversations:
            # Se não houver conversas, simula o fechamento de uma conversa inexistente
            conv_id = str(uuid.uuid4())
            payload = {
                "type": "CLOSE_CONVERSATION",
                "timestamp": get_timestamp(),
                "data": {"id": conv_id},
            }
        else:
            conv_id = random.choice(open_conversations)
            payload = {
                "type": "CLOSE_CONVERSATION",
                "timestamp": get_timestamp(),
                "data": {"id": conv_id},
            }
            open_conversations.remove(conv_id)

    print("Enviando payload:", payload)
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        print("Resposta:", response.status_code, response.text)
    except Exception as e:
        print("Erro ao enviar:", e)

    # Aguarda 30 segundos para enviar o próximo evento
    time.sleep(5)
