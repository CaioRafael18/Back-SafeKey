from rest_framework import serializers
from safekey.models import Reservation
from safekey.serializers.user_serializers import UserSerializer
from safekey.serializers.room_serializers import RoomSerializer
from safekey.models import User, Room

class ReservationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    room = RoomSerializer(read_only=True)
    responsible = UserSerializer(read_only=True, allow_null=True)

    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="user", write_only=True
    )
    room_id = serializers.PrimaryKeyRelatedField(
        queryset=Room.objects.all(), source="room", write_only=True
    )
    responsible_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source="responsible", write_only=True, allow_null=True
    )

    class Meta:
        model = Reservation
        fields = [
            "id",
            "date_schedulling",
            "start_time",
            "end_time",
            "reason",
            "commentary",
            "status",
            "deleted_at",
            "user", "user_id",
            "responsible", "responsible_id",
            "room", "room_id",
        ]

    def validate(self, data):
        # Valida conflitos antes de salvar no banco
        temp_reservation = Reservation(**data)  # Cria um objeto temporário com os dados recebidos
        temp_reservation.check_reservation()  # Chama a validação do modelo
        return data