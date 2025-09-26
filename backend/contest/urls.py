from django.urls import path
from . import views

app_name = 'contest'

urlpatterns = [
    # =============================================================================
    # ENDPOINTS PÚBLICOS (RESTful naming)
    # =============================================================================
    
    # Crear concursante (inscripción)
    path('contestants/', views.register_contestant, name='contestants'),
    
    # Verificación de email y creación de contraseña
    path('verification/', views.verify_email_and_set_password, name='verification'),
    
    # =============================================================================
    # ENDPOINTS ADMIN (protegidos)
    # =============================================================================
    
    # Listar concursantes (con filtros y paginación)
    path('admin/contestants/', views.list_contestants, name='admin-contestants'),
    
    # Gestión de ganador (GET: ver, POST: sortear)
    path('admin/winner/', views.winner_view, name='admin-winner'),
]
