from rest_framework import serializers
from safekey.models import User, UserType, Room, Reservation
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    # Definindo o modelo e pegando todos os campos
    class Meta:
        model = User
        fields = '__all__'

class UsersTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = '__all__'

class CustomTokenObtainPairSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Verificando autenticação do usuário
        user = authenticate(request=self.context.get('request'), email=email, password=password)

        # Se o usuário não existe
        if user is None:
            raise serializers.ValidationError("Credenciais inválidas.")
        
        # Criando token e refresh token
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        access_token['userType'] = user.type.type

        # Se o usuário for autenticado com sucesso, retorne os dados necessários
        user_serializer = UserSerializer(user)
        id_type = user_serializer.data['type']
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