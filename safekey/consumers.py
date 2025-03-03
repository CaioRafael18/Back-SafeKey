import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RoomStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Define o grupo WebSocket corretamente
        self.room_group_name = "room_status_channel"

        # Adiciona o WebSocket ao grupo
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Aceita a conexão WebSocket
        await self.accept()

    async def disconnect(self, close_code):
        # Remove o WebSocket do grupo ao desconectar
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        
    # Método para enviar notificações WebSocket
    async def send_room_status_update(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))
