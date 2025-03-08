from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from safekey.models import User
from safekey.serializers.user_serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all() # buscando todos os dados do meu usuário
    serializer_class = UserSerializer
            
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Obtém o usuário a ser deletado
        self.perform_destroy(instance)
        return Response({"detail": "Usuário deletado com sucesso"}, status=204)
    
    @action(detail=False, methods=['POST', 'PUT', 'PATCH', 'DELETE'])
    def listUsers(self, request):
        if request.method == 'POST':
            return self.create_users(request)
        elif request.method in ['PUT', 'PATCH']:
            return self.update_users(request)
        elif request.method == 'DELETE':
            return self.delete_users(request)
        return Response({"error": "Método não permitido"}, status=405)

    def create_users(self, request):
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            # Valida e salva os dados
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            return Response(serializer.data, status=201)
        return Response({"error": "Os dados devem ser uma lista"}, status=400)

    def update_users(self, request):
        if isinstance(request.data, list):
            instances = []
            errors = []

            for user_data in request.data:
                user_id = user_data.get("id")
                if not user_id:
                    errors.append({"error": "ID é obrigatório para atualizar", "data": user_data})
                    continue

                try:
                    instance = User.objects.get(id=user_id)
                    serializer = self.get_serializer(instance, data=user_data, partial=True)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                    instances.append(serializer.data)
                except User.DoesNotExist:
                    errors.append({"error": f"Usuário com ID {user_id} não encontrado."})

            if errors:
                return Response({"updated": instances, "errors": errors}, status=207)
            return Response(instances, status=200)
        return Response({"error": "Os dados devem ser uma lista"}, status=400)

    def delete_users(self, request):
        if isinstance(request.data, list):
            ids = [user.get("id") for user in request.data if "id" in user]
            if ids:
                User.objects.filter(id__in=ids).delete()
                return Response({"detail": "Usuários deletados com sucesso"}, status=204)
            return Response({"error": "Nenhum ID válido fornecido"}, status=400)
        return Response({"error": "Os dados devem ser uma lista"}, status=400)