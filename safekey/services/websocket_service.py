from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class WebSocketService:
    def send_type_status_update(type, updated):
        channel_layer = get_channel_layer()
        message = f"Status da {updated} {type.id} atualizado para {type.status}."
        async_to_sync(channel_layer.group_send)(
            "status_channel",
            {
                "type": "send_status_update",
                "message": message,
                "updated": updated
            }
        )