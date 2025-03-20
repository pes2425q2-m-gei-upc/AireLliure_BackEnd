from django.db import models
from django.conf import settings
from django.utils import timezone

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, primary_key=True)
    descripcio = models.TextField()
    class Meta: 
        abstract = True
    def __str__(self):
        return self.nombre 

class DificultatEsportiva(Categoria):
    pass

class AccesibilitatRespiratoria(Categoria):
    pass

class Usuari(models.Model):
    correu = models.EmailField(primary_key=True)
    password = models.CharField(max_length=255)
    nom = models.CharField(max_length=255)
    estat = models.CharField(max_length=255)
    punts = models.IntegerField(default=0)
    deshabilitador = models.ForeignKey('Admin', on_delete=models.CASCADE, null=True, blank=True)
    about = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nom
    
class Admin(Usuari):
    pass

class Bloqueig(models.Model):
    id = models.AutoField(primary_key=True)
    bloqueja = models.ForeignKey(Usuari, on_delete=models.CASCADE, related_name='bloquejants')
    bloquejat = models.ForeignKey(Usuari, on_delete=models.CASCADE, related_name='bloquejats')

    class Meta: 
        constraints = [
            models.UniqueConstraint(fields=['bloqueja', 'bloquejat'], name='bloqueig_unic')
        ]
    def __str__(self):
        return f"{self.bloqueja} + {self.bloquejat}"


class Amistat(models.Model):
    id = models.AutoField(primary_key=True)
    solicita = models.ForeignKey(Usuari, on_delete=models.CASCADE, related_name='solicitades')
    accepta = models.ForeignKey(Usuari, on_delete=models.CASCADE, related_name='acceptades', null=True, blank=True)
    data_inici = models.DateTimeField(auto_now_add=True)
    data_final = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['solicita', 'accepta'], name='amistat_unic'),
            models.CheckConstraint(check=models.Q(data_inici__lte=models.F('data_final')), name='data_inici_menor_data_final')
        ]
    def __str__(self):
        return f"{self.solicita} + {self.accepta}"
    
class Ruta(models.Model):
    id = models.AutoField(primary_key=True)
    descripcio = models.TextField()
    nom = models.CharField(max_length=255)
    dist_km = models.FloatField()
    punts = models.ManyToManyField('Punt', related_name='rutes')
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(dist_km__gte=0), name='dist_km_valid')
        ]

    def __str__(self):
        return self.nom

class Valoracio(models.Model):
    id = models.AutoField(primary_key=True)
    usuari = models.ForeignKey(Usuari, on_delete=models.CASCADE)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    puntuacio = models.IntegerField()
    comentari = models.TextField()

    class Meta: 
        constraints = [
            models.UniqueConstraint(fields=['usuari', 'ruta'], name='valoracio_unic'),
            models.CheckConstraint(check=models.Q(puntuacio__gte=0) & models.Q(puntuacio__lte=5), name='puntuacio_valida')
        ]

    def __str__(self):
        return f"{self.usuari} + {self.ruta}"
    
class Recompensa(models.Model):
    id = models.AutoField(primary_key=True)
    usuari = models.ForeignKey(Usuari, on_delete=models.CASCADE)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)
    data_recompensa = models.DateTimeField(auto_now_add=True)
    punts = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['usuari', 'data_recompensa'], name='recompensa_unic')
        ]

    def __str__(self):
        return f"{self.usuari} + {self.ruta}"
    
class AssignaDificultatEsportiva(models.Model):
    id = models.AutoField(primary_key=True)
    usuari = models.ForeignKey('Admin', on_delete=models.CASCADE)
    dificultat = models.ForeignKey(DificultatEsportiva, on_delete=models.CASCADE)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['usuari', 'ruta'], name='assigna_dificultat_unic')
        ]

    def __str__(self):
        return f"{self.usuari} + {self.dificultat} + {self.ruta}"

class AssignaAccesibilitatRespiratoria(models.Model):
    id = models.AutoField(primary_key=True)
    usuari = models.ForeignKey('Admin', on_delete=models.CASCADE)
    accesibilitat = models.ForeignKey(AccesibilitatRespiratoria, on_delete=models.CASCADE)
    ruta = models.ForeignKey(Ruta, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['usuari', 'ruta'], name='assigna_accesibilitat_unic')
        ]

    def __str__(self):
        return f"{self.usuari} + {self.accesibilitat} + {self.ruta}"

class Xat(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class XatIndividual(Xat):
    usuari1 = models.ForeignKey(Usuari, on_delete=models.CASCADE, related_name='xats_com_usuari1', null=True, blank=True)
    usuari2 = models.ForeignKey(Usuari, on_delete=models.CASCADE, related_name='xats_com_usuari2', null=True, blank=True)
    def __str__(self):
        return f"{self.usuari1} + {self.usuari2}"

class XatGrupal(Xat):
    creador = models.ForeignKey(Usuari, on_delete=models.CASCADE, related_name='xats_creadors', null=True, blank=True)
    descripció = models.TextField()
    membres = models.ManyToManyField(Usuari, related_name='xats_membres')

    def __str__(self):
        return f"{self.creador} + {self.descripció}"
    
class Invitacio(models.Model):

    CHOICES = [
        ('pendent', 'Pendent'),
        ('resolta', 'Resolta')
    ]
    id = models.AutoField(primary_key=True)
    destinatari = models.ForeignKey(Usuari, on_delete=models.CASCADE, related_name='invitacions_recibides')
    creador = models.ForeignKey(Usuari, on_delete=models.CASCADE, related_name='invitacions_enviades')
    estat = models.CharField(max_length=255, choices=CHOICES)
    xat = models.ForeignKey(XatGrupal, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['destinatari', 'xat'], name='invitacio_unic')
        ]

    def __str__(self):
        return f"{self.destinatari} + {self.creador} + {self.xat}"

class Missatge(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    xat = models.ForeignKey(Xat, on_delete=models.CASCADE)
    autor = models.ForeignKey(Usuari, on_delete=models.CASCADE, related_name='missatges_autors', null=True, blank=True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-data']

class EventDeCalendari(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)
    descripció = models.TextField()
    data_inici = models.DateTimeField(default=timezone.now)
    data_fi = models.DateTimeField(default=timezone.now)
    creador = models.ForeignKey(Usuari, on_delete=models.CASCADE, name= 'creador_event', null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(data_inici__lte=models.F('data_fi')), name='event_data_inici_menor_data_fi')
        ]

class EventDeCalendariPrivat(EventDeCalendari):
    xat = models.ForeignKey(Xat, on_delete=models.CASCADE, name='xat_event', null=True, blank=True)

class EventDeCalendariPublic(EventDeCalendari): 
    limit = models.IntegerField()

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(limit__gte=0), name='limit_valid')
        ]

class Apuntat(models.Model):
    id = models.AutoField(primary_key=True)
    usuari = models.ForeignKey(Usuari, on_delete=models.CASCADE)
    event = models.ForeignKey(EventDeCalendariPublic, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['usuari', 'event'], name='apuntat_unic')
        ]

class Punt(models.Model):
    latitud = models.FloatField()
    longitud = models.FloatField()
    altitud = models.FloatField(default=0)
    index_qualitat_aire = models.FloatField(blank=True, null=True)

    class Meta: 
        constraints = [
            models.UniqueConstraint(fields=['latitud', 'longitud'], name='punt_unic')
        ]
    
    def __str__(self):
        return f"{self.latitud} + {self.longitud} + {self.altitud} + {self.index_qualitat_aire}"

class EstacioQualitatAire(Punt):
    nom_estacio = models.CharField(max_length=255)
    descripcio = models.CharField(max_length=255)

class ActivitatCultural(Punt):
    nom_activitat = models.CharField(max_length=255)
    descripcio = models.CharField(max_length=255)
    data_inici = models.DateField()
    data_fi = models.DateField(null=True, blank=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(data_inici__lte=models.F('data_fi')), name='activitat_data_inici_menor_data_fi')
        ]

class Contaminant(models.Model):
    nom = models.CharField(max_length=255)
    informacio = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.nom} + {self.informacio}"

class Presencia(models.Model):
    punt = models.ForeignKey(Punt, on_delete=models.CASCADE)
    contaminant = models.ForeignKey(Contaminant, on_delete=models.CASCADE)
    data = models.DateField()
    valor = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.punt} + {self.contaminant} + {self.data} + {self.valor}"
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['punt', 'contaminant', 'data'], name='presencia_unic'),
            models.CheckConstraint(check=models.Q(valor__gte=0), name='valor_valid')
        ]

class JobExecution(models.Model):
    name = models.CharField(max_length=100, unique=True)
    last_run = models.DateTimeField(default=timezone.now)