from django.urls import path
from . import views

urlpatterns = [
    # Aquí irán tus URLs cuando las necesites
    
    # CATEGORIA
    path('categories/', views.get_categories, name='get_categories'),
    
    # DIFICULTAT ESPORTIVA
    path('dificultats-esportiva/', views.get_dificultats_esportiva, name='get_dificultats_esportiva'),
    path('dificultats-esportiva/<str:pk>/', views.get_dificultat_esportiva, name='get_dificultat_esportiva'),
    path('dificultats-esportiva/create/', views.create_dificultat_esportiva, name='create_dificultat_esportiva'),
    path('dificultats-esportiva/<str:pk>/update/', views.update_dificultat_esportiva, name='update_dificultat_esportiva'),
    path('dificultats-esportiva/<str:pk>/delete/', views.delete_dificultat_esportiva, name='delete_dificultat_esportiva'),
    
    #ACCESIBILITAT RESPIRATORIA
    path('accessibilitats-respiratoria/', views.get_accessibilitats_respiratoria, name='get_accessibilitats_respiratoria'),
    path('accessibilitats-respiratoria/<str:pk>/', views.get_accessibilitat_respiratoria, name='get_accessibilitat_respiratoria'),
    path('accessibilitats-respiratoria/create/', views.create_accessibilitat_respiratoria, name='create_accessibilitat_respiratoria'),
    path('accessibilitats-respiratoria/<str:pk>/update/', views.update_accessibilitat_respiratoria, name='update_accessibilitat_respiratoria'),
    path('accessibilitats-respiratoria/<str:pk>/delete/', views.delete_accessibilitat_respiratoria, name='delete_accessibilitat_respiratoria'),
    
    #USUARI
    path('usuaris/', views.get_usuaris, name='get_usuaris'),
    path('usuaris/<str:pk>/', views.get_usuari, name='get_usuari'),
    path('usuaris/create/', views.create_usuari, name='create_usuari'),
    path('usuaris/<str:pk>/update/', views.update_usuari, name='update_usuari'),
    path('usuaris/<str:pk>/delete/', views.delete_usuari, name='delete_usuari'),
    
    #ADMIN
    path('admins/', views.get_admins, name='get_admins'),
    path('admins/<str:pk>/', views.get_admin, name='get_admin'),
    path('admins/create/', views.create_admin, name='create_admin'),
    path('admins/<str:pk>/update/', views.update_admin, name='update_admin'),
    path('admins/<str:pk>/delete/', views.delete_admin, name='delete_admin'),
    
    #BLOQUEIG
    path('bloqueigs/', views.get_bloqueigs, name='get_bloqueigs'),
    path('bloqueigs/<int:pk>/', views.get_bloqueig, name='get_bloqueig'),
    path('bloqueigs/create/', views.create_bloqueig, name='create_bloqueig'),
    path('bloqueigs/<int:pk>/update/', views.update_bloqueig, name='update_bloqueig'),
    path('bloqueigs/<int:pk>/delete/', views.delete_bloqueig, name='delete_bloquei'),
    
    #AMISTAT
    path('amistats/', views.get_amistats, name='get_amistats'),
    path('amistats/<int:pk>/', views.get_amistat, name='get_amistat'),
    path('amistats/create/', views.create_amistat, name='create_amistat'),
    path('amistats/<int:pk>/update/', views.update_amistat, name='update_amistat'),
    path('amistats/<int:pk>/delete/', views.delete_amistat, name='delete_amistat'),
    
    #RUTA
    
    path('rutas/', views.get_rutas, name='get_rutas'),
    path('rutas/<int:pk>/', views.get_ruta, name='get_ruta'),
    path('rutas/create/', views.create_ruta, name='create_ruta'),
    path('rutas/<int:pk>/update/', views.update_ruta, name='update_ruta'),
    path('rutas/<int:pk>/delete/', views.delete_ruta, name='delete_ruta'),
    
    #VALORACIO
    path('valoracions/', views.get_valoracions, name='get_valoracions'),
    path('valoracions/<int:pk>/', views.get_valoracio, name='get_valoracio'),
    path('valoracions/create/', views.create_valoracio, name='create_valoracio'),
    path('valoracions/<int:pk>/update/', views.update_valoracio, name='update_valoracio'),
    path('valoracions/<int:pk>/delete/', views.delete_valoracio, name='delete_valoracio'),
    
    #RECOMPENSA
    path('recompenses/', views.get_recompenses, name='get_recompenses'),
    path('recompenses/<int:pk>/', views.get_recompensa, name='get_recompensa'),
    path('recompenses/create/', views.create_recompensa, name='create_recompensa'),
    path('recompenses/<int:pk>/update/', views.update_recompensa, name='update_recompensa'),
    path('recompenses/<int:pk>/delete/', views.delete_recompensa, name='delete_recompensa'),
    
    

]