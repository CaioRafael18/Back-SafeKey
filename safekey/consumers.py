import json
from channels.generic.websocket import AsyncWebsocketConsumer

class RoomStatusConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "room_status_channel"

        # Adiciona o WebSocket ao grupo
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Aceita a conexão WebSocket
        await self.accept()

        # Envia uma mensagem para todos notificando que um novo usuário entrou
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_room_status_update",
                "message": "Usuário se conectou ao WebSocket."
            }
        )

    async def disconnect(self, close_code):
        # Remove o WebSocket do grupo ao desconectar
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # Notifica os outros usuários que alguém saiu
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "send_room_status_update",
                "message": "Usuário se desconectou do WebSocket."
            }
        )
        
    # Método para enviar notificações WebSocket
    async def send_room_status_update(self, event):
        reservations = event["reservations"]  # Recebe a lista de todas as reservas
        await self.send(text_data=json.dumps({"reservations": reservations}))

