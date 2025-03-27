from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from safekey.models import Room
from safekey.serializers.room_serializers import RoomSerializer
from rest_framework.permissions import AllowAny
from safekey.services.websocket_service import WebSocketService

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Obtém a sala a ser deletada
        self.perform_destroy(instance)
        return Response({"detail": "Sala deletada com sucesso"}, status=204)
    
    # Rota para atualizar status da sala
    def update_room_status(self, room, status, status_key):
        room.status = status
        room.status_key = status_key
        room.save()
        WebSocketService.send_type_status_update(room, "sala")

    # Rota publica para exibir todas as salas
    @action(detail=False, methods=['GET'], permission_classes=[AllowAny])
    def public(self, request, pk=None):
        room = Room.objects.all()
        serializer = RoomSerializer(room, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['POST', 'PUT', 'PATCH', 'DELETE'])
    def list_rooms(self, request):
        if request.method == 'POST':
            return self.create_rooms(request)
        elif request.method in ['PUT', 'PATCH']:
            return self.update_rooms(request)
        elif request.method == 'DELETE':
            return self.delete_rooms(request)
        return Response({"error": "Método não permitido"}, status=405)

    def create_rooms(self, request):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=201)
        return Response({"error": "Os dados devem ser uma lista"}, status=400)

    def update_rooms(self, request):
        if isinstance(request.data, list):
            instances = []
            errors = []

            for room_data in request.data:
                room_id = room_data.get("id")
                if not room_id:
                    errors.append({"error": "ID é obrigatório para atualizar", "data": room_data})
                    continue

                try:
                    instance = Room.objects.get(id=room_id)
                    serializer = self.get_serializer(instance, data=room_data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    instances.append(serializer.data)
                except Room.DoesNotExist:
                    errors.append({"error": f"Sala com ID {room_id} não encontrado."})

            if errors:
                return Response({"updated": instances, "errors": errors}, status=207)
            return Response(instances, status=200)
        return Response({"error": "Os dados devem ser uma lista"}, status=400)

    def delete_rooms(self, request):
        if isinstance(request.data, list):
            ids = [room.get("id") for room in request.data if "id" in room]
            if ids:
                Room.objects.filter(id__in=ids).delete()
                return Response({"detail": "Salas deletadas com sucesso"}, status=204)
            return Response({"error": "Nenhum ID válido fornecido"}, status=400)
        return Response({"error": "Os dados devem ser uma lista"}, status=400)