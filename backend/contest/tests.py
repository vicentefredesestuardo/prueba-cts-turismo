from django.test import TestCase, override_settings
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
import uuid

from .models import Contestant, EmailVerificationToken, WinnerDraw


class ContestAPITests(TestCase):
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.client = APIClient()
        
        # Crear superusuario para pruebas admin
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@test.com',
            password='adminpass123'
        )

    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        CELERY_TASK_ALWAYS_EAGER=True,
        CELERY_TASK_EAGER_PROPAGATES=True,
    )
    def test_registro_exitoso(self):
        """Registro exitoso de concursante"""
        url = reverse('contest:contestants')
        data = {
            'first_name': 'Juan',
            'last_name': 'Pérez',
            'email': 'juan@test.com',
            'phone': '+56912345678'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contestant.objects.count(), 1)
        self.assertEqual(EmailVerificationToken.objects.count(), 1)
        
        contestant = Contestant.objects.first()
        self.assertEqual(contestant.first_name, 'Juan')
        self.assertEqual(contestant.last_name, 'Pérez')
        self.assertEqual(contestant.email, 'juan@test.com')
        self.assertEqual(contestant.phone, '+56912345678')
        self.assertFalse(contestant.is_verified)

    def test_verificacion_token_invalido(self):
        """Verificación con token inválido"""
        url = reverse('contest:verification')
        data = {
            'token': str(uuid.uuid4()),
            'password': 'password123',
            'password_confirm': 'password123'
        }
        
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_requiere_jwt(self):
        """Admin requiere autenticación JWT"""
        url = reverse('contest:admin-contestants')
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend', 
        CELERY_TASK_ALWAYS_EAGER=True,
        CELERY_TASK_EAGER_PROPAGATES=True,
    )
    def test_sorteo_solo_una_vez(self):
        """Sorteo solo se puede realizar una vez"""
        # Crear concursante verificado
        contestant = Contestant.objects.create(
            first_name='María',
            last_name='González',
            email='maria@test.com',
            phone='+56987654321',
            is_verified=True
        )
        
        # Autenticar como admin
        self.client.force_authenticate(user=self.admin_user)
        
        url = reverse('contest:admin-winner')
        
        # Primer sorteo debe ser exitoso
        response1 = self.client.post(url)
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # Segundo sorteo debe fallar
        response2 = self.client.post(url)
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
