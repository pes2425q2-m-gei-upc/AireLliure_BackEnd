from django import forms
from .models import *

class CategoriaForm(forms.Form):
    model = Categoria
    fields = '__all__'

class DificultatEsportivaForm(forms.Form):
    model = DificultatEsportiva
    fields = '__all__'

class AccesibilitatRespiratoriaForm(forms.Form):
    model = AccesibilitatRespiratoria
    fields = '__all__'

class UsuariForm(forms.Form):
    model = Usuari
    fields = '__all__'

class AdminForm(forms.Form):
    model = Admin
    fields = '__all__'

class BloqueigForm(forms.Form):
    model = Bloqueig
    fields = '__all__'

class AmistatForm(forms.Form):
    model = Amistat
    fields = '__all__'

class RutaForm(forms.Form):
    model = Ruta
    fields = '__all__'

class ValoracioForm(forms.Form):
    model = Valoracio
    fields = '__all__'

class RecompensaForm(forms.Form):
    model = Recompensa
    fields = '__all__'

class AssignaDificultatEsportivaForm(forms.Form):
    model = AssignaDificultatEsportiva
    fields = '__all__'

class AssignaAccesibilitatRespiratoriaForm(forms.Form):
    model = AssignaAccesibilitatRespiratoria
    fields = '__all__'

class XatForm(forms.Form):
    model = Xat
    fields = '__all__'

class XatIndividualForm(forms.Form):
    model = XatIndividual
    fields = '__all__'

class XatGrupalForm(forms.Form):
    model = XatGrupal
    fields = '__all__'

class InvitacioForm(forms.Form):
    model = Invitacio
    fields = '__all__'

class MissatgeForm(forms.Form):
    model = Missatge
    fields = '__all__'

class EventDeCalendariForm(forms.Form):
    model = EventDeCalendari
    fields = '__all__'

class EventDeCalendariPrivatForm(forms.Form):
    model = EventDeCalendariPrivat
    fields = '__all__'

class EventDeCalendariPublicForm(forms.Form):
    model = EventDeCalendariPublic
    fields = '__all__'

class ApuntatForm(forms.Form):
    model = Apuntat
    fields = '__all__'

class PuntForm(forms.Form):
    model = Punt
    fields = '__all__'

class EstacioQualitatAireForm(forms.Form):
    model = EstacioQualitatAire
    fields = '__all__'

class ActivitatCulturalForm(forms.Form):
    model = ActivitatCultural
    fields = '__all__'
    
class ContaminantForm(forms.Form):
    model = Contaminant
    fields = '__all__'

class PresenciaForm(forms.Form):
    model = Presencia
    fields = '__all__'