from rest_framework import serializers
from safekey.models import Reservation

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

    def validate(self, data):
        # Valida conflitos antes de salvar no banco
        temp_reservation = Reservation(**data)  # Cria um objeto temporário com os dados recebidos
        temp_reservation.check_reservation()  # Chama a validação do modelo
        return data