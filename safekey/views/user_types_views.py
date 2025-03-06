from rest_framework import viewsets
from rest_framework.response import Response
from safekey.models import UserType
from safekey.serializers import UsersTypesSerializer

class UsersTypesViewSet(viewsets.ModelViewSet):
    queryset = UserType.objects.all()
    serializer_class = UsersTypesSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()  # Obtém o tipo do usuário a ser deletado
        self.perform_destroy(instance)
        return Response({"detail": "Tipo de usuário deletado com sucesso"}, status=204)