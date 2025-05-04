from django.contrib import admin

from app.models import (
    AccesibilitatRespiratoria,
    ActivitatCultural,
    Admin,
    Amistat,
    Apuntat,
    AssignaAccesibilitatRespiratoria,
    AssignaDificultatEsportiva,
    Bloqueig,
    Contaminant,
    DificultatEsportiva,
    EstacioQualitatAire,
    EventDeCalendari,
    EventDeCalendariPrivat,
    EventDeCalendariPublic,
    Invitacio,
    Missatge,
    Presencia,
    Punt,
    Recompensa,
    Ruta,
    Usuari,
    Valoracio,
    Xat,
    XatGrupal,
    XatIndividual,
)

# Importamos todos los modelos

# Registrar cada modelo de manera básica
# admin.site.register(NombreDelModelo)

# O si quieres personalizar la vista del admin:
# @admin.register(NombreDelModelo)
# class NombreDelModeloAdmin(admin.ModelAdmin):
#     # Campos que se mostrarán en la lista
#     list_display = ['campo1', 'campo2', 'campo3']
#     # Campos por los que se puede buscar
#     search_fields = ['campo1', 'campo2']
#     # Campos por los que se puede filtrar
#     list_filter = ['campo1']


@admin.register(DificultatEsportiva)
class DificultatEsportivaAdmin(admin.ModelAdmin):
    pass


@admin.register(AccesibilitatRespiratoria)
class AccesibilitatRespiratoriaAdmin(admin.ModelAdmin):
    pass


@admin.register(Usuari)
class UsuariAdmin(admin.ModelAdmin):
    pass


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    pass


@admin.register(Bloqueig)
class BloqueigAdmin(admin.ModelAdmin):
    pass


@admin.register(Amistat)
class AmistatAdmin(admin.ModelAdmin):
    pass


@admin.register(Invitacio)
class InvitacioAdmin(admin.ModelAdmin):
    pass


@admin.register(Apuntat)
class ApuntatAdmin(admin.ModelAdmin):
    pass


@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    pass


@admin.register(Valoracio)
class ValoracioAdmin(admin.ModelAdmin):
    pass


@admin.register(Recompensa)
class RecompensaAdmin(admin.ModelAdmin):
    pass


@admin.register(AssignaDificultatEsportiva)
class AssignaDificultatEsportivaAdmin(admin.ModelAdmin):
    pass


@admin.register(AssignaAccesibilitatRespiratoria)
class AssignaAccesibilitatRespiratoriaAdmin(admin.ModelAdmin):
    pass


@admin.register(Xat)
class XatAdmin(admin.ModelAdmin):
    pass


@admin.register(XatIndividual)
class XatIndividualAdmin(admin.ModelAdmin):
    pass


@admin.register(XatGrupal)
class XatGrupalAdmin(admin.ModelAdmin):
    pass


@admin.register(Missatge)
class MissatgeAdmin(admin.ModelAdmin):
    pass


@admin.register(EventDeCalendari)
class EventDeCalendariAdmin(admin.ModelAdmin):
    pass


@admin.register(EventDeCalendariPrivat)
class EventDeCalendariPrivatAdmin(admin.ModelAdmin):
    pass


@admin.register(EventDeCalendariPublic)
class EventDeCalendariPublicAdmin(admin.ModelAdmin):
    pass


@admin.register(Punt)
class PuntAdmin(admin.ModelAdmin):
    pass


@admin.register(EstacioQualitatAire)
class EstacioQualitatAireAdmin(admin.ModelAdmin):
    pass


@admin.register(ActivitatCultural)
class ActivitatCulturalAdmin(admin.ModelAdmin):
    pass


@admin.register(Contaminant)
class ContaminantAdmin(admin.ModelAdmin):
    pass


@admin.register(Presencia)
class PresenciaAdmin(admin.ModelAdmin):
    pass
