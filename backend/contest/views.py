from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.db.models import Q
from django.db.models.functions import Random
from .models import Contestant, EmailVerificationToken, WinnerDraw
from .serializers import (
    ContestantRegistrationSerializer,
    EmailVerificationSerializer,
    ContestantSerializer,
    WinnerDrawSerializer
)
from .tasks import send_verification_email, send_winner_notification


# =============================================================================
# ENDPOINTS PÚBLICOS
# =============================================================================

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_contestant(request):
    """Inscripción al concurso"""
    # Normalizar datos antes de enviar al serializer
    data = request.data.copy()
    for k in ('first_name', 'last_name', 'second_last_name', 'email', 'phone'):
        if k in data and isinstance(data[k], str):
            data[k] = data[k].strip()
    if 'email' in data:
        data['email'] = data['email'].lower()
    
    serializer = ContestantRegistrationSerializer(data=data)
    if serializer.is_valid():
        contestant = serializer.save()
        
        # Crear token de verificación
        token = EmailVerificationToken.objects.create(contestant=contestant)
        
        # Enviar email de verificación (asíncrono)
        send_verification_email.delay(contestant.id, str(token.token))
        
        return Response({
            'message': '¡Gracias por registrarte! Revisa tu correo para verificar tu cuenta.',
            'contestant_id': contestant.id
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def verify_email_and_set_password(request):
    """Verificar email y crear contraseña"""
    serializer = EmailVerificationSerializer(data=request.data)
    if serializer.is_valid():
        contestant = serializer.save()
        
        return Response({
            'message': 'Tu cuenta ha sido activada. Ya estás participando en el sorteo.',
            'contestant': ContestantSerializer(contestant).data
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =============================================================================
# ENDPOINTS ADMIN
# =============================================================================

@api_view(['GET'])
@permission_classes([IsAdminUser])
def list_contestants(request):
    """Listar concursantes con paginación y filtros"""
    contestants = Contestant.objects.all().order_by('-created_at')
    
    # Filtros
    verified = request.GET.get('verified')
    if verified is not None:
        contestants = contestants.filter(is_verified=verified.lower() == 'true')
    
    search = request.GET.get('search')
    if search:
        contestants = contestants.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(second_last_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    # Paginación
    try:
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 50))
    except ValueError:
        page, page_size = 1, 50
    page = max(page, 1)
    page_size = max(min(page_size, 200), 1)  # límite superior sano

    start = (page - 1) * page_size
    end = start + page_size
    
    total = contestants.count()
    serializer = ContestantSerializer(contestants[start:end], many=True)
    
    return Response({
        'count': total,
        'page': page,
        'page_size': page_size,
        'contestants': serializer.data
    })


@api_view(['GET', 'POST'])
@permission_classes([IsAdminUser])
def winner_view(request):
    """
    GET: Ver el ganador actual
    POST: Sortear ganador (solo uno permitido)
    """
    if request.method == 'POST':
        # SORTEAR GANADOR
        # Verificar que no haya ganador previo
        if WinnerDraw.objects.exists():
            return Response({
                'error': 'Ya se ha realizado el sorteo. Solo se permite un ganador.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Seleccionar ganador aleatorio
        winner = Contestant.objects.filter(is_verified=True).order_by(Random()).first()
        if not winner:
            return Response({
                'error': 'No hay concursantes verificados para el sorteo.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Crear registro del sorteo
        winner_draw = WinnerDraw.objects.create(contestant=winner)
        
        # Enviar email al ganador (asíncrono)
        send_winner_notification.delay(winner.id)
        
        return Response({
            'message': f'¡Ganador seleccionado! {winner.full_name}',
            'winner': WinnerDrawSerializer(winner_draw).data
        }, status=status.HTTP_201_CREATED)
    
    elif request.method == 'GET':
        # VER GANADOR ACTUAL
        try:
            winner = WinnerDraw.objects.select_related('contestant').latest('drawn_at')
            return Response({
                'winner': WinnerDrawSerializer(winner).data
            })
        except WinnerDraw.DoesNotExist:
            return Response({
                'message': 'Aún no se ha realizado el sorteo.'
            }, status=status.HTTP_404_NOT_FOUND)
