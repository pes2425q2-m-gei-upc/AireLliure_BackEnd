# flake8: noqa: F403, F405

from django import forms

from .models import *


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = "__all__"


class DificultatEsportivaForm(forms.ModelForm):
    class Meta:
        model = DificultatEsportiva
        fields = "__all__"


class AccesibilitatRespiratoriaForm(forms.ModelForm):
    class Meta:
        model = AccesibilitatRespiratoria
        fields = "__all__"


class UsuariForm(forms.ModelForm):
    class Meta:
        model = Usuari
        fields = "__all__"


class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = "__all__"


class BloqueigForm(forms.ModelForm):
    class Meta:
        model = Bloqueig
        fields = "__all__"


class AmistatForm(forms.ModelForm):
    class Meta:
        model = Amistat
        fields = "__all__"


class RutaForm(forms.ModelForm):
    class Meta:
        model = Ruta
        fields = "__all__"


class ValoracioForm(forms.ModelForm):
    class Meta:
        model = Valoracio
        fields = "__all__"


class RecompensaForm(forms.ModelForm):
    class Meta:
        model = Recompensa
        fields = "__all__"


class AssignaDificultatEsportivaForm(forms.ModelForm):
    class Meta:
        model = AssignaDificultatEsportiva
        fields = "__all__"


class AssignaAccesibilitatRespiratoriaForm(forms.ModelForm):
    class Meta:
        model = AssignaAccesibilitatRespiratoria
        fields = "__all__"


class XatForm(forms.ModelForm):
    class Meta:
        model = Xat
        fields = "__all__"


class XatIndividualForm(forms.ModelForm):
    class Meta:
        model = XatIndividual
        fields = "__all__"


class XatGrupalForm(forms.ModelForm):
    class Meta:
        model = XatGrupal
        fields = "__all__"


class InvitacioForm(forms.ModelForm):
    class Meta:
        model = Invitacio
        fields = "__all__"


class MissatgeForm(forms.ModelForm):
    class Meta:
        model = Missatge
        fields = "__all__"


class EventDeCalendariForm(forms.ModelForm):
    class Meta:
        model = EventDeCalendari
        fields = "__all__"


class EventDeCalendariPrivatForm(forms.ModelForm):
    class Meta:
        model = EventDeCalendariPrivat
        fields = "__all__"


class EventDeCalendariPublicForm(forms.ModelForm):
    class Meta:
        model = EventDeCalendariPublic
        fields = "__all__"


class ApuntatForm(forms.ModelForm):
    class Meta:
        model = Apuntat
        fields = "__all__"


class PuntForm(forms.ModelForm):
    class Meta:
        model = Punt
        fields = "__all__"


class EstacioQualitatAireForm(forms.ModelForm):
    class Meta:
        model = EstacioQualitatAire
        fields = "__all__"


class ActivitatCulturalForm(forms.ModelForm):
    class Meta:
        model = ActivitatCultural
        fields = "__all__"


class ContaminantForm(forms.ModelForm):
    class Meta:
        model = Contaminant
        fields = "__all__"


class PresenciaForm(forms.ModelForm):
    class Meta:
        model = Presencia
        fields = "__all__"


class IndexQualitatAireForm(forms.ModelForm):
    class Meta:
        model = IndexQualitatAire
        fields = "__all__"
