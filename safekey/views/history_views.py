from rest_framework import viewsets
from rest_framework.response import Response
from safekey.models import History
from safekey.serializers.history_serializers import HistorySerializer

class HistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object() # Obtém o historico a ser deletado
        self.perform_destroy(instance)
        return Response({"detail": "Historico deletado com sucesso"}, status=204)