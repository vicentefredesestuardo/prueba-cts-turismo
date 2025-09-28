from django.urls import path
from . import views

app_name = 'contest'

urlpatterns = [
    # Endpoints públicos
    path('contestants/', views.register_contestant, name='contestants'),
    path('verification/', views.verify_email_and_set_password, name='verification'),
    
    # Endpoints admin
    path('admin/contestants/', views.list_contestants, name='admin-contestants'),
    path('admin/winner/', views.winner_view, name='admin-winner'),
]
