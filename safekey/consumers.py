import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RoomStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Adiciona o WebSocket ao grupo
        self.room_name = "room_status_channel"
        self.room_group_name = f"room_status_{self.room_name}"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Aceita a conexão WebSocket
        await self.accept()

    async def disconnect(self, close_code):
        # Desconecta o WebSocket
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    # Método para enviar notificações em tempo real
    async def send_room_status_update(self, event):
        # Envia uma notificação para o cliente WebSocket
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))