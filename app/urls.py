from django.urls import path

from . import views

urlpatterns = [
    # Aquí irán tus URLs cuando las necesites
    # CATEGORIA
    path("categories/", views.get_categories, name="get_categories"),
    # DIFICULTAT ESPORTIVA
    path(
        "dificultats-esportiva/",
        views.get_dificultats_esportiva,
        name="get_dificultats_esportiva",
    ),
    path(
        "dificultats-esportiva/create/",
        views.create_dificultat_esportiva,
        name="create_dificultat_esportiva",
    ),
    path(
        "dificultats-esportiva/<str:pk>/",
        views.get_dificultat_esportiva,
        name="get_dificultat_esportiva",
    ),
    path(
        "dificultats-esportiva/<str:pk>/update/",
        views.update_dificultat_esportiva,
        name="update_dificultat_esportiva",
    ),
    path(
        "dificultats-esportiva/<str:pk>/delete/",
        views.delete_dificultat_esportiva,
        name="delete_dificultat_esportiva",
    ),
    # ACCESIBILITAT RESPIRATORIA
    path(
        "accessibilitats-respiratoria/",
        views.get_accessibilitats_respiratoria,
        name="get_accessibilitats_respiratoria",
    ),
    path(
        "accessibilitats-respiratoria/create/",
        views.create_accessibilitat_respiratoria,
        name="create_accessibilitat_respiratoria",
    ),
    path(
        "accessibilitats-respiratoria/<str:pk>/",
        views.get_accessibilitat_respiratoria,
        name="get_accessibilitat_respiratoria",
    ),
    path(
        "accessibilitats-respiratoria/<str:pk>/update/",
        views.update_accessibilitat_respiratoria,
        name="update_accessibilitat_respiratoria",
    ),
    path(
        "accessibilitats-respiratoria/<str:pk>/delete/",
        views.delete_accessibilitat_respiratoria,
        name="delete_accessibilitat_respiratoria",
    ),
    # USUARI
    path("login/", views.login_usuari, name="login_usuari"),
    path("usuaris/", views.get_usuaris, name="get_usuaris"),
    path(
        "deshabilitats/",
        views.get_all_usuaris_deshabilitats,
        name="get_all_usuaris_deshabilitats",
    ),
    path(
        "habilitats/",
        views.get_all_usuaris_habilitats,
        name="get_all_usuaris_habilitats",
    ),
    path("usuaris/create/", views.create_usuari, name="create_usuari"),
    path("usuaris/<str:pk>/", views.get_usuari, name="get_usuari"),
    path("usuaris/<str:pk>/update/", views.update_usuari, name="update_usuari"),
    path("usuaris/<str:pk>/delete/", views.delete_usuari, name="delete_usuari"),
    path(
        "usuaris/<str:correu_deshabilitador>/deshabilitar/<str:correu_usuari>/",
        views.deshabilitar_usuari,
        name="deshabilitar_usuari",
    ),
    path(
        "usuaris/<str:correu_usuari>/rehabilitar/",
        views.rehabilitar_usuari,
        name="rehabilitar_usuari",
    ),
    # ADMIN
    path("admins/", views.get_admins, name="get_admins"),
    path("admins/create/", views.create_admin, name="create_admin"),
    path("admins/<str:pk>/", views.get_admin, name="get_admin"),
    path("admins/<str:pk>/update/", views.update_admin, name="update_admin"),
    path("admins/<str:pk>/delete/", views.delete_admin, name="delete_admin"),
    # BLOQUEIG
    path("bloqueigs/", views.get_bloqueigs, name="get_bloqueigs"),
    path("bloqueigs/<int:pk>/", views.get_bloqueig, name="get_bloqueig"),
    path("bloqueigs/create/", views.create_bloqueig, name="create_bloqueig"),
    path("bloqueigs/<int:pk>/update/", views.update_bloqueig, name="update_bloqueig"),
    path("bloqueigs/<int:pk>/delete/", views.delete_bloqueig, name="delete_bloqueig"),
    path(
        "bloqueigs/usuari/<str:pk>/",
        views.get_bloquigs_usuari,
        name="get_bloquigs_usuari",
    ),
    # AMISTAT
    path("amistats/", views.get_amistats, name="get_amistats"),
    path("amistats/<int:pk>/", views.get_amistat, name="get_amistat"),
    path("amistats/create/", views.create_amistat, name="create_amistat"),
    path("amistats/<int:pk>/update/", views.update_amistat, name="update_amistat"),
    path("amistats/<int:pk>/delete/", views.delete_amistat, name="delete_amistat"),
    path("amistats/usuari/<str:pk>/", views.get_amics_usuari, name="get_amics_usuari"),
    # FLUX DE SOLICITUDS I ACCEPTACIONS DE AMISTATS
    path(
        "amistats/usuari/<str:pk>/rebudes/",
        views.get_solicituds_rebudes,
        name="get_solicituds_rebudes",
    ),
    path(
        "amistats/usuari/<str:pk>/enviades/",
        views.get_solicituds_enviades,
        name="get_solicituds_enviades",
    ),
    path(
        "amistats/usuari/<str:pk>/basics/",
        views.get_usuaris_basics,
        name="get_usuaris_basics",
    ),
    # RUTA
    path("rutas/", views.get_rutas, name="get_rutas"),
    path("rutas/<int:pk>/", views.get_ruta, name="get_ruta"),
    path("rutas/create/", views.create_ruta, name="create_ruta"),
    path("rutas/<int:pk>/update/", views.update_ruta, name="update_ruta"),
    path("rutas/<int:pk>/delete/", views.delete_ruta, name="delete_ruta"),
    path("rutas/<int:pk>/info/", views.get_all_info_ruta, name="get_all_info_ruta"),
    # VALORACIO
    path("valoracions/", views.get_valoracions, name="get_valoracions"),
    path("valoracions/<int:pk>/", views.get_valoracio, name="get_valoracio"),
    path("valoracions/create/", views.create_valoracio, name="create_valoracio"),
    path(
        "valoracions/<int:pk>/update/", views.update_valoracio, name="update_valoracio"
    ),
    path(
        "valoracions/<int:pk>/delete/", views.delete_valoracio, name="delete_valoracio"
    ),
    # RECOMPENSA
    path("recompenses/", views.get_recompenses, name="get_recompenses"),
    path("recompenses/<int:pk>/", views.get_recompensa, name="get_recompensa"),
    path("recompenses/create/", views.create_recompensa, name="create_recompensa"),
    path(
        "recompenses/<int:pk>/update/",
        views.update_recompensa,
        name="update_recompensa",
    ),
    path(
        "recompenses/<int:pk>/delete/",
        views.delete_recompensa,
        name="delete_recompensa",
    ),
    # ASSIGNACIO ESPORTIVA
    path(
        "assignacions-esportiva/",
        views.get_assignacions_esportiva,
        name="get_assignacions_esportiva",
    ),
    path(
        "assignacions-esportiva/<int:pk>/",
        views.get_assignacio_esportiva,
        name="get_assignacio_esportiva",
    ),
    path(
        "assignacions-esportiva/create/",
        views.create_assignacio_esportiva,
        name="create_assignacio_esportiva",
    ),
    path(
        "assignacions-esportiva/<int:pk>/update/",
        views.update_assignacio_esportiva,
        name="update_assignacio_esportiva",
    ),
    path(
        "assignacions-esportiva/<int:pk>/delete/",
        views.delete_assignacio_esportiva,
        name="delete_assignacio_esportiva",
    ),
    # ASSIGNACIO ACCESIBILITAT RESPIRATORIA
    path(
        "assignacions-accesibilitat-respiratoria/",
        views.get_assignacions_accesibilitat_respiratoria,
        name="get_assignacions_accesibilitat_respiratoria",
    ),
    path(
        "assignacions-accesibilitat-respiratoria/<int:pk>/",
        views.get_assignacio_accesibilitat_respiratoria,
        name="get_assignacio_accesibilitat_respiratoria",
    ),
    path(
        "assignacions-accesibilitat-respiratoria/create/",
        views.create_assignacio_accesibilitat_respiratoria,
        name="create_assignacio_accesibilitat_respiratoria",
    ),
    path(
        "assignacions-accesibilitat-respiratoria/<int:pk>/update/",
        views.update_assignacio_accesibilitat_respiratoria,
        name="update_assignacio_accesibilitat_respiratoria",
    ),
    path(
        "assignacions-accesibilitat-respiratoria/<int:pk>/delete/",
        views.delete_assignacio_accesibilitat_respiratoria,
        name="delete_assignacio_accesibilitat_respiratoria",
    ),
    # XAT
    path("xats/", views.get_xats, name="get_xats"),
    path("xats/<int:pk>/", views.get_xat, name="get_xat"),
    path("xats/create/", views.create_xat, name="create_xat"),
    path("xats/<int:pk>/update/", views.update_xat, name="update_xat"),
    path("xats/<int:pk>/delete/", views.delete_xat, name="delete_xat"),
    path("xats/usuari/<str:pk>/", views.get_xats_usuari, name="get_xats_usuari"),
    # XAT INDIVIDUAL
    path("xats-individual/", views.get_xats_individual, name="get_xats_individual"),
    path(
        "xats-individual/<int:pk>/", views.get_xat_individual, name="get_xat_individual"
    ),
    path(
        "xats-individual/create/",
        views.create_xat_individual,
        name="create_xat_individual",
    ),
    path(
        "xats-individual/<int:pk>/update/",
        views.update_xat_individual,
        name="update_xat_individual",
    ),
    path(
        "xats-individual/<int:pk>/delete/",
        views.delete_xat_individual,
        name="delete_xat_individual",
    ),
    # XAT GRUPAL
    path("xats-grupal/", views.get_xats_grupal, name="get_xats_grupal"),
    path("xats-grupal/<int:pk>/", views.get_xat_grupal, name="get_xat_grupal"),
    path("xats-grupal/create/", views.create_xat_grupal, name="create_xat_grupal"),
    path(
        "xats-grupal/<int:pk>/update/",
        views.update_xat_grupal,
        name="update_xat_grupal",
    ),
    path(
        "xats-grupal/<int:pk>/delete/",
        views.delete_xat_grupal,
        name="delete_xat_grupal",
    ),
    path(
        "xats-grupal/<int:pk>/afegir-usuari/<str:pkuser>/",
        views.afegir_usuari_xat,
        name="afegir_usuari_xat",
    ),
    path(
        "xats-grupal/<int:pk>/eliminar-usuari/<str:pkuser>/",
        views.eliminar_usuari_xat,
        name="eliminar_usuari_xat",
    ),
    # INVITACIO
    path("invitacions/", views.get_invitacions, name="get_invitacions"),
    path("invitacions/<int:pk>/", views.get_invitacio, name="get_invitacio"),
    path("invitacions/create/", views.create_invitacio, name="create_invitacio"),
    path(
        "invitacions/<int:pk>/update/", views.update_invitacio, name="update_invitacio"
    ),
    path(
        "invitacions/<int:pk>/delete/", views.delete_invitacio, name="delete_invitacio"
    ),
    # MISSATGE
    path("missatges/", views.get_missatges, name="get_missatges"),
    path("missatges/<int:pk>/", views.get_missatge, name="get_missatge"),
    path("missatges/create/", views.create_missatge, name="create_missatge"),
    path("missatges/<int:pk>/update/", views.update_missatge, name="update_missatge"),
    path("missatges/<int:pk>/delete/", views.delete_missatge, name="delete_missatge"),
    # EVENT DE CALENDARI
    path(
        "events-de-calendari/",
        views.get_events_de_calendari,
        name="get_events_de_calendari",
    ),
    path(
        "events-de-calendari/<int:pk>/",
        views.get_event_de_calendari,
        name="get_event_de_calendari",
    ),
    path(
        "events-de-calendari/create/",
        views.create_event_de_calendari,
        name="create_event_de_calendari",
    ),
    path(
        "events-de-calendari/<int:pk>/update/",
        views.update_event_de_calendari,
        name="update_event_de_calendari",
    ),
    path(
        "events-de-calendari/<int:pk>/delete/",
        views.delete_event_de_calendari,
        name="delete_event_de_calendari",
    ),
    # EVENT DE CALENDARI PRIVAT
    path(
        "events-de-calendari-privats/",
        views.get_events_de_calendari_privats,
        name="get_events_de_calendari_privats",
    ),
    path(
        "events-de-calendari-privats/<int:pk>/",
        views.get_event_de_calendari_privat,
        name="get_event_de_calendari_privat",
    ),
    path(
        "events-de-calendari-privats/create/",
        views.create_event_de_calendari_privat,
        name="create_event_de_calendari_privat",
    ),
    path(
        "events-de-calendari-privats/<int:pk>/update/",
        views.update_event_de_calendari_privat,
        name="update_event_de_calendari_privat",
    ),
    path(
        "events-de-calendari-privats/<int:pk>/delete/",
        views.delete_event_de_calendari_privat,
        name="delete_event_de_calendari_privat",
    ),
    # EVENT DE CALENDARI PUBLIC
    path(
        "events-de-calendari-publics/",
        views.get_events_de_calendari_publics,
        name="get_events_de_calendari_publics",
    ),
    path(
        "events-de-calendari-publics/<int:pk>/",
        views.get_event_de_calendari_public,
        name="get_event_de_calendari_public",
    ),
    path(
        "events-de-calendari-publics/create/",
        views.create_event_de_calendari_public,
        name="create_event_de_calendari_public",
    ),
    path(
        "events-de-calendari-publics/<int:pk>/update/",
        views.update_event_de_calendari_public,
        name="update_event_de_calendari_public",
    ),
    path(
        "events-de-calendari-publics/<int:pk>/delete/",
        views.delete_event_de_calendari_public,
        name="delete_event_de_calendari_public",
    ),
    # APUNTAT
    path("apuntats/", views.get_apuntats, name="get_apuntats"),
    path("apuntats/<int:pk>/", views.get_apuntat, name="get_apuntat"),
    path("apuntats/create/", views.create_apuntat, name="create_apuntat"),
    path("apuntats/<int:pk>/update/", views.update_apuntat, name="update_apuntat"),
    path("apuntats/<int:pk>/delete/", views.delete_apuntat, name="delete_apuntat"),
    # PUNT
    path("punts/", views.get_punts, name="get_punts"),
    path("punts/<int:pk>/", views.get_punt, name="get_punt"),
    path("punts/create/", views.create_punt, name="create_punt"),
    path("punts/<int:pk>/update/", views.update_punt, name="update_punt"),
    path("punts/<int:pk>/delete/", views.delete_punt, name="delete_punt"),
    # ESTACIO QUALITAT AIRE
    path(
        "estacions-qualitat-aire/",
        views.get_estacions_qualitat_aire,
        name="get_estacions_qualitat_aire",
    ),
    path(
        "estacions-qualitat-aire/<int:pk>/",
        views.get_estacio_qualitat_aire,
        name="get_estacio_qualitat_aire",
    ),
    path(
        "estacions-qualitat-aire/create/",
        views.create_estacio_qualitat_aire,
        name="create_estacio_qualitat_aire",
    ),
    path(
        "estacions-qualitat-aire/<int:pk>/update/",
        views.update_estacio_qualitat_aire,
        name="update_estacio_qualitat_aire",
    ),
    path(
        "estacions-qualitat-aire/<int:pk>/delete/",
        views.delete_estacio_qualitat_aire,
        name="delete_estacio_qualitat_aire",
    ),
    # ACTIVITAT CULTURAL
    path(
        "activitats-culturals/",
        views.get_activitats_culturals,
        name="get_activitats_culturals",
    ),
    path(
        "activitats-culturals/<int:pk>/",
        views.get_activitat_cultural,
        name="get_activitat_cultural",
    ),
    path(
        "activitats-culturals/create/",
        views.create_activitat_cultural,
        name="create_activitat_cultural",
    ),
    path(
        "activitats-culturals/<int:pk>/update/",
        views.update_activitat_cultural,
        name="update_activitat_cultural",
    ),
    path(
        "activitats-culturals/<int:pk>/delete/",
        views.delete_activitat_cultural,
        name="delete_activitat_cultural",
    ),
    # CONTAMINANT
    path("contaminants/", views.get_contaminants, name="get_contaminants"),
    path("contaminants/<int:pk>/", views.get_contaminant, name="get_contaminant"),
    path("contaminants/create/", views.create_contaminant, name="create_contaminant"),
    path(
        "contaminants/<int:pk>/update/",
        views.update_contaminant,
        name="update_contaminant",
    ),
    path(
        "contaminants/<int:pk>/delete/",
        views.delete_contaminant,
        name="delete_contaminant",
    ),
    # PRESENCIA
    path("presencies/", views.get_presencies, name="get_presencies"),
    path("presencies/<int:pk>/", views.get_presencia, name="get_presencia"),
    path("presencies/create/", views.create_presencia, name="create_presencia"),
    path(
        "presencies/<int:pk>/update/", views.update_presencia, name="update_presencia"
    ),
    path(
        "presencies/<int:pk>/delete/", views.delete_presencia, name="delete_presencia"
    ),
    path(
        "presencies/punt/<int:pk>/",
        views.get_presencies_punt,
        name="get_presencies_punt",
    ),
    path(
        "presencies/punt/<str:lon>/<str:lat>/",
        views.get_presencies_punt_lon_lat,
        name="get_presencies_punt_lon_lat",
    ),
    # DADES OBERTES
    path(
        "actualitzar/rutes",
        views.actualitzar_rutes_bd,
        name="actualitzar_rutes",
    ),
    path(
        "actualitzar/estacions_qualitat_aire",
        views.actualitzar_estacions_qualitat_aire_bd,
        name="actualitzar_estacions_qualitat_aire",
    ),
    path(
        "actualitzar/activitats_culturals",
        views.actualitzar_activitats_culturals_bd,
        name="actualitzar_activitats_culturals",
    ),
    # RANKING
    path(
        "ranking-usuaris-all/",
        views.obtenir_ranking_usuaris_all,
        name="obtenir_ranking_usuaris_all",
    ),
    path(
        "ranking-usuari-amics/<str:pk>/",
        views.obtenir_ranking_usuari_amics,
        name="obtenir_ranking_usuari_amics",
    ),
    # Normalitzacio
    path(
        "normalitzar-valor-contaminant-presencia/<int:pk>/",
        views.normalitzar_valor_contaminant,
        name="normalitzar_valor_contaminant",
    ),  # pk de la presencia
    path(
        "normalitzar-valor-contaminant-punt/<int:pk>/",
        views.normalitzar_valor_contaminant_punt,
        name="normalitzar_valor_contaminant_punt",
    ),  # pk del punt
    # INDEX QUALITAT DE L'AIRE TAULA
    path(
        "index-qualitat-aire-taula/",
        views.get_index_qualitat_aire_taula,
        name="get_index_qualitat_aire_taula",
    ),
    path(
        "index-qualitat-aire-taula-contaminant/<int:pk>/",
        views.get_index_qualitat_aire_taula_contaminant,
        name="get_index_qualitat_aire_taula_contaminant",
    ),
    path(
        "index-qualitat-aire-taula/create/",
        views.create_index_qualitat_aire_taula,
        name="create_index_qualitat_aire_taula",
    ),
    path(
        "index-qualitat-aire-taula/<int:pk>/update/",
        views.update_index_qualitat_aire_taula,
        name="update_index_qualitat_aire_taula",
    ),
    path(
        "index-qualitat-aire-taula/<int:pk>/delete/",
        views.delete_index_qualitat_aire_taula,
        name="delete_index_qualitat_aire_taula",
    ),
    # ASSIGNACIO DIFICULTAT ESPORTIVA
    path(
        "assig-esportiva/<int:pk_ruta>/",
        views.get_asig_esportiva,
        name="get_asig_esportiva",
    ),
    # ASSIGNACIO ACCESIBILITAT RESPIRATORIA
    path(
        "assig-acc-resp/<int:pk_ruta>/",
        views.get_asig_respiratoria,
        name="get_asig_respiratoria",
    ),
]
