from .models import *
from rest_framework import serializers

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class DificultatEsportivaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DificultatEsportiva
        fields = ['nombre', 'descripcio']

class AccesibilitatRespiratoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccesibilitatRespiratoria
        fields = ['nombre', 'descripcio']

class UsuariSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuari
        fields = '__all__'

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'
        
class BloqueigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bloqueig
        fields = '__all__'

class AmistatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amistat
        fields = '__all__'

class ValoracioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valoracio
        fields = '__all__'

class RecompensaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recompensa
        fields = '__all__'

class AssignaDificultatEsportivaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignaDificultatEsportiva
        fields = '__all__'

class AssignaAccesibilitatRespiratoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignaAccesibilitatRespiratoria
        fields = '__all__'

class XatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Xat
        fields = '__all__'

class XatIndividualSerializer(serializers.ModelSerializer):
    class Meta:
        model = XatIndividual
        fields = '__all__'

class XatGrupalSerializer(serializers.ModelSerializer):
    class Meta:
        model = XatGrupal
        fields = '__all__'

class InvitacioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invitacio
        fields = '__all__'

class MissatgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Missatge
        fields = '__all__'

class EventDeCalendariSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventDeCalendari
        fields = '__all__'

class EventDeCalendariPrivatSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventDeCalendariPrivat
        fields = '__all__'

class EventDeCalendariPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventDeCalendariPublic
        fields = '__all__'

class ApuntatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apuntat
        fields = '__all__'

class PuntSerializer(serializers.ModelSerializer):
    class Meta:
        model = Punt
        fields = '__all__'

class RutaSerializer(serializers.ModelSerializer):
    id = serializers.CharField(required=False)
    class Meta:
        model = Ruta
        fields = '__all__'

class EstacioQualitatAireSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstacioQualitatAire
        fields = '__all__'

class ActivitatCulturalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivitatCultural
        fields = '__all__'

class ContaminantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contaminant
        fields = '__all__'

class PresenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Presencia
        fields = '__all__'

class JobExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobExecution
        fields = '__all__'