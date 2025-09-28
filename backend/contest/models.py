import uuid
from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.utils import timezone

phone_validator = RegexValidator(
    regex=r'^\+?[1-9]\d{7,14}$',
    message="Ingrese un teléfono válido en formato internacional (E.164), ej: +56912345678."
)

def default_token_expiry():
    return timezone.now() + timedelta(hours=2)

class Contestant(models.Model):
    first_name = models.CharField("Nombre(s)", max_length=50)
    last_name = models.CharField("Apellido Paterno", max_length=30)
    second_last_name = models.CharField("Apellido Materno", max_length=30, blank=True)
    email = models.EmailField(unique=True)  # ← MANTÉN unique=True
    phone = models.CharField(max_length=16, validators=[phone_validator])
    is_verified = models.BooleanField(default=False)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def full_name(self):
        names = [self.first_name, self.last_name]
        if self.second_last_name:
            names.append(self.second_last_name)
        return " ".join(names)

    def __str__(self):
        return f"{self.full_name} <{self.email}>"
        
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Concursante"
        verbose_name_plural = "Concursantes"

class EmailVerificationToken(models.Model):
    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE, related_name="tokens")
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=default_token_expiry)
    used_at = models.DateTimeField(null=True, blank=True)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def __str__(self):
        return f"Token {self.token} for {self.contestant.email}"

class WinnerDraw(models.Model):
    contestant = models.ForeignKey(Contestant, on_delete=models.CASCADE)
    drawn_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.contestant.email} @ {self.drawn_at}"
