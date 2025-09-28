from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from django.db.models.functions import Lower

from .models import Contestant, EmailVerificationToken, WinnerDraw
from .utils import normalize_contestant_fields


class ContestantRegistrationSerializer(serializers.ModelSerializer):
    """Registro inicial de concursantes"""

    class Meta:
        model = Contestant
        fields = ["first_name", "last_name", "second_last_name", "email", "phone"]

    def validate(self, attrs):
        return normalize_contestant_fields(attrs)

    def validate_email(self, value):
        if Contestant.objects.filter(email__iexact=value.strip()).exists():
            raise serializers.ValidationError("Este correo ya está inscrito en el concurso.")
        return value


class ContestantSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Contestant
        fields = [
            "id", "first_name", "last_name", "second_last_name", "full_name",
            "email", "phone", "is_verified", "created_at",
        ]
        read_only_fields = ["id", "is_verified", "created_at"]


class EmailVerificationSerializer(serializers.Serializer):
    """
    Verifica token y setea contraseña en un solo paso.
    Si prefieres 2 pasos, separa en VerifyTokenSerializer y SetPasswordSerializer.
    """
    token = serializers.UUIDField()
    password = serializers.CharField(write_only=True, min_length=8, trim_whitespace=False)
    password_confirm = serializers.CharField(write_only=True, min_length=8, trim_whitespace=False)

    def validate(self, data):
        if data["password"] != data["password_confirm"]:
            raise serializers.ValidationError("Las contraseñas no coinciden.")
        validate_password(data["password"])
        return data

    def validate_token(self, value):
        try:
            token_obj = EmailVerificationToken.objects.select_related("contestant").get(
                token=value, used_at__isnull=True
            )
        except EmailVerificationToken.DoesNotExist:
            raise serializers.ValidationError("Token de verificación inválido.")
        if token_obj.is_expired():
            raise serializers.ValidationError("El token de verificación ha expirado.")
        return token_obj  
    
    def create(self, validated_data):
        """
        La view hará serializer.save() para ejecutar esta lógica:
        - marcar verificado
        - crear/vincular User con password
        - marcar token.used_at
        """
        token_obj: EmailVerificationToken = validated_data["token"]
        contestant = token_obj.contestant

        # Verifica concursante
        if not contestant.is_verified:
            contestant.is_verified = True
            contestant.save(update_fields=["is_verified"])

        # Crea o vincula User y setea password
        if not contestant.user:
            user, _ = User.objects.get_or_create(
                username=contestant.email.lower(),
                defaults={
                    'email': contestant.email.lower(),
                    'is_active': True,
                }
            )
            # Vincula el user al contestant
            contestant.user = user
            contestant.save(update_fields=['user'])
        else:
            user = contestant.user

        user.set_password(validated_data["password"])
        user.save()
        if contestant.user_id != user.id:
            contestant.user = user
            contestant.save(update_fields=["user"])

        # Marca token como usado
        token_obj.used_at = timezone.now()
        token_obj.save(update_fields=["used_at"])

        return contestant 

class EmailVerificationTokenSerializer(serializers.ModelSerializer):
    contestant_name = serializers.CharField(source="contestant.full_name", read_only=True)
    contestant_email = serializers.CharField(source="contestant.email", read_only=True)
    is_expired = serializers.SerializerMethodField()

    class Meta:
        model = EmailVerificationToken
        fields = [
            "id", "contestant", "contestant_name", "contestant_email",
            "token", "created_at", "expires_at", "used_at", "is_expired",
        ]
        read_only_fields = ["token", "created_at", "expires_at", "used_at"]

    def get_is_expired(self, obj):
        return obj.is_expired()


class WinnerDrawSerializer(serializers.ModelSerializer):
    contestant_name = serializers.CharField(source="contestant.full_name", read_only=True)
    contestant_email = serializers.CharField(source="contestant.email", read_only=True)
    contestant_phone = serializers.CharField(source="contestant.phone", read_only=True)

    class Meta:
        model = WinnerDraw
        fields = ["id", "contestant", "contestant_name", "contestant_email", "contestant_phone", "drawn_at"]
        read_only_fields = ["drawn_at"]


class DrawWinnerSerializer(serializers.Serializer):
    """
    Ejecuta el sorteo. Si prefieres, hazlo en la view y usa solo WinnerDrawSerializer para la respuesta.
    """
    message = serializers.CharField(read_only=True)
    winner = WinnerDrawSerializer(read_only=True)

    def create(self, validated_data):
        from django.db.models.functions import Random

        eligible = Contestant.objects.filter(is_verified=True).order_by(Random())
        winner_contestant = eligible.first()
        if not winner_contestant:
            raise serializers.ValidationError("No hay concursantes elegibles para el sorteo.")

        winner_draw = WinnerDraw.objects.create(contestant=winner_contestant)
        return {
            "message": f"¡Ganador seleccionado! {winner_contestant.full_name}",
            "winner": winner_draw,
        }
