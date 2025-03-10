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
    
    #ASSIGNACIO ESPORTIVA
    path('assignacions-esportiva/', views.get_assignacions_esportiva, name='get_assignacions_esportiva'),
    path('assignacions-esportiva/<int:pk>/', views.get_assignacio_esportiva, name='get_assignacio_esportiva'),
    path('assignacions-esportiva/create/', views.create_assignacio_esportiva, name='create_assignacio_esportiva'),
    path('assignacions-esportiva/<int:pk>/update/', views.update_assignacio_esportiva, name='update_assignacio_esportiva'),
    path('assignacions-esportiva/<int:pk>/delete/', views.delete_assignacio_esportiva, name='delete_assignacio_esportiva'),
    
    #ASSIGNACIO ACCESIBILITAT RESPIRATORIA
    path('assignacions-accesibilitat-respiratoria/', views.get_assignacions_accesibilitat_respiratoria, name='get_assignacions_accesibilitat_respiratoria'),
    path('assignacions-accesibilitat-respiratoria/<int:pk>/', views.get_assignacio_accesibilitat_respiratoria, name='get_assignacio_accesibilitat_respiratoria'),
    path('assignacions-accesibilitat-respiratoria/create/', views.create_assignacio_accesibilitat_respiratoria, name='create_assignacio_accesibilitat_respiratoria'),
    path('assignacions-accesibilitat-respiratoria/<int:pk>/update/', views.update_assignacio_accesibilitat_respiratoria, name='update_assignacio_accesibilitat_respiratoria'),
    path('assignacions-accesibilitat-respiratoria/<int:pk>/delete/', views.delete_assignacio_accesibilitat_respiratoria, name='delete_assignacio_accesibilitat_respiratoria'),

    #XAT
    path('xats/', views.get_xats, name='get_xats'),
    path('xats/<int:pk>/', views.get_xat, name='get_xat'),
    path('xats/create/', views.create_xat, name='create_xat'),
    path('xats/<int:pk>/update/', views.update_xat, name='update_xat'),
    path('xats/<int:pk>/delete/', views.delete_xat, name='delete_xat'),
    
    #XAT INDIVIDUAL
    path('xats-individual/', views.get_xats_individual, name='get_xats_individual'),
    path('xats-individual/<int:pk>/', views.get_xat_individual, name='get_xat_individual'),
    path('xats-individual/create/', views.create_xat_individual, name='create_xat_individual'),
    path('xats-individual/<int:pk>/update/', views.update_xat_individual, name='update_xat_individual'),
    path('xats-individual/<int:pk>/delete/', views.delete_xat_individual, name='delete_xat_individual'),
    
    #XAT GRUPAL
    path('xats-grupal/', views.get_xats_grupal, name='get_xats_grupal'),
    path('xats-grupal/<int:pk>/', views.get_xat_grupal, name='get_xat_grupal'),
    path('xats-grupal/create/', views.create_xat_grupal, name='create_xat_grupal'),
    path('xats-grupal/<int:pk>/update/', views.update_xat_grupal, name='update_xat_grupal'),
    path('xats-grupal/<int:pk>/delete/', views.delete_xat_grupal, name='delete_xat_grupal'),
    
    #INVITACIO
    path('invitacions/', views.get_invitacions, name='get_invitacions'),
    path('invitacions/<int:pk>/', views.get_invitacio, name='get_invitacio'),
    path('invitacions/create/', views.create_invitacio, name='create_invitacio'),
    path('invitacions/<int:pk>/update/', views.update_invitacio, name='update_invitacio'),
    path('invitacions/<int:pk>/delete/', views.delete_invitacio, name='delete_invitacio'),
    
    #MISSATGE
    path('missatges/', views.get_missatges, name='get_missatges'),
    path('missatges/<int:pk>/', views.get_missatge, name='get_missatge'),
    path('missatges/create/', views.create_missatge, name='create_missatge'),
    path('missatges/<int:pk>/update/', views.update_missatge, name='update_missatge'),
    path('missatges/<int:pk>/delete/', views.delete_missatge, name='delete_missatge'),
    
    #EVENT DE CALENDARI
    path('events-de-calendari/', views.get_events_de_calendari, name='get_events_de_calendari'),
    path('events-de-calendari/<int:pk>/', views.get_event_de_calendari, name='get_event_de_calendari'),
    path('events-de-calendari/create/', views.create_event_de_calendari, name='create_event_de_calendari'),
    path('events-de-calendari/<int:pk>/update/', views.update_event_de_calendari, name='update_event_de_calendari'),
    path('events-de-calendari/<int:pk>/delete/', views.delete_event_de_calendari, name='delete_event_de_calendari'),
    
    #EVENT DE CALENDARI PRIVAT
    path('events-de-calendari-privats/', views.get_events_de_calendari_privats, name='get_events_de_calendari_privats'),
    path('events-de-calendari-privats/<int:pk>/', views.get_event_de_calendari_privat, name='get_event_de_calendari_privat'),
    path('events-de-calendari-privats/create/', views.create_event_de_calendari_privat, name='create_event_de_calendari_privat'),
    path('events-de-calendari-privats/<int:pk>/update/', views.update_event_de_calendari_privat, name='update_event_de_calendari_privat'),
    path('events-de-calendari-privats/<int:pk>/delete/', views.delete_event_de_calendari_privat, name='delete_event_de_calendari_privat'),
    
    #EVENT DE CALENDARI PUBLIC
    path('events-de-calendari-publics/', views.get_events_de_calendari_publics, name='get_events_de_calendari_publics'),
    path('events-de-calendari-publics/<int:pk>/', views.get_event_de_calendari_public, name='get_event_de_calendari_public'),
    path('events-de-calendari-publics/create/', views.create_event_de_calendari_public, name='create_event_de_calendari_public'),
    path('events-de-calendari-publics/<int:pk>/update/', views.update_event_de_calendari_public, name='update_event_de_calendari_public'),
    path('events-de-calendari-publics/<int:pk>/delete/', views.delete_event_de_calendari_public, name='delete_event_de_calendari_public'),
    
    
    
    
]
