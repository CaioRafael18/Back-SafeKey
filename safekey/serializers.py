from rest_framework import serializers
from safekey.models import User, UserType, Room, Reservation
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed

class UsersTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = '__all__'
        
class UserSerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(queryset=UserType.objects.all())  # Para POST, aceita apenas o ID do type

    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'type']

    def create(self, validated_data):
        # Armazenando a senha do usuário criado como hash no banco
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def to_representation(self, instance):
        # retorna o objeto completo do tipo de usuário (com id e type)
        representation = super().to_representation(instance)
        representation['type'] = UsersTypesSerializer(instance.type).data
        return representation

class CustomTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)

        # Se não encontrar o usuário(retornar None)
        if not user:
            raise AuthenticationFailed({'detail': 'Credenciais inválidas. Verifique seu e-mail e senha.'})

        # Criando token e refresh token
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        access_token['userType'] = user.type.type

        # Se o usuário for autenticado com sucesso, retorne os dados necessários
        user_serializer = UserSerializer(user)
        id_type = user_serializer.data['type']['id']
        type_object = UserType.objects.get(id=id_type)
        user_type_serializer = UsersTypesSerializer(type_object)

        # Substituir o campo 'type' no user_serializer.data com os dados completos do 'user_type_serializer.data'
        user_data = user_serializer.data
        user_data['type'] = user_type_serializer.data

        return {
            'refresh_token': str(refresh_token),
            'access_token': str(access_token),
            'user': user_data,
        }

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'

    def validate(self, data):
        # Valida conflitos antes de salvar no banco
        temp_reservation = Reservation(**data)  # Cria um objeto temporário com os dados recebidos
        temp_reservation.check_reservation()  # Chama a validação do modelo
        return data