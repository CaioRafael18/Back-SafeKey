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
                "message": "Usuário desconectou do WebSocket."
            }
        )
        
    # Método para enviar notificações WebSocket
    async def send_room_status_update(self, event):
        message = event['message']
        print(f"Recebendo mensagem do grupo: {message}")

        # Verifica se 'updated' está presente no evento
        response_data = {'message': message}
        if 'updated' in event:
            response_data['updated'] = event['updated']
        
        await self.send(text_data=json.dumps(response_data))