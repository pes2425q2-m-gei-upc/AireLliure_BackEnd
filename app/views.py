from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import *
from .serializers import *
from .forms import *
from django.shortcuts import get_object_or_404
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from .utils import actualitzar_rutes, actualitzar_estacions_qualitat_aire, actualitzar_activitats_culturals
from django.db.models import Q



# ------- funcions auxiliars -----------------------------------------------------------------------------

def actualitza_recompensa_usuari(usuari):
    user = get_object_or_404(Usuari, pk=usuari)
    recompenses = Recompensa.objects.filter(usuari=user)
    punts = 0
    for recompensa in recompenses:
        punts += recompensa.punts
    user.punts = punts
    user.save()
    
# ---------------- LA PART DE CATEGORIA ------------------------------------------------------------------

@api_view(['GET'])
def get_categories(request):
    difficulties_ = DificultatEsportiva.objects.all()
    accessibilities_ = AccesibilitatRespiratoria.objects.all()
    #Agafem totes i el que fem ara a continuacio es les postejem.
    difficulties = DificultatEsportivaSerializer(difficulties_, many=True)
    accessibilities = AccesibilitatRespiratoriaSerializer(accessibilities_, many=True)
    return Response({
        'difficulties': difficulties.data,
        'accessibilities': accessibilities.data
    }, status=status.HTTP_200_OK)

#DIFICULTAT ESPORTIVA ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_dificultats_esportiva(request):
    difficulties = DificultatEsportiva.objects.all()
    serializer = DificultatEsportivaSerializer(difficulties, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_dificultat_esportiva(request, pk):
    difficulty = get_object_or_404(DificultatEsportiva, pk=pk)
    serializer = DificultatEsportivaSerializer(difficulty)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def create_dificultat_esportiva(request):
    data = {
        'nombre': request.data.get('nombre'),
        'descripcio': request.data.get('descripcio'),
    }
    form = DificultatEsportivaForm(data=data)
    if form.is_valid():
        dificultat = form.save()
        serializer = DificultatEsportivaSerializer(dificultat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def update_dificultat_esportiva(request, pk):
    difficulty = get_object_or_404(DificultatEsportiva, pk=pk)
    serializer = DificultatEsportivaSerializer(difficulty, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_dificultat_esportiva(request, pk):
    difficulty = get_object_or_404(DificultatEsportiva, pk=pk)
    if difficulty is not None:
        difficulty.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)

#ACCESIBILITAT RESPIRATORIA ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_accessibilitats_respiratoria(request):
    accessibilities = AccesibilitatRespiratoria.objects.all()
    serializer = AccesibilitatRespiratoriaSerializer(accessibilities, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_accessibilitat_respiratoria(request, pk):
    accessibility = get_object_or_404(AccesibilitatRespiratoria, pk=pk)
    serializer = AccesibilitatRespiratoriaSerializer(accessibility)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST', 'GET'])
def create_accessibilitat_respiratoria(request):
    data = {
        'nombre': request.data.get('nombre'),
        'descripcio': request.data.get('descripcio')
    }
    form = AccesibilitatRespiratoriaForm(data=data)
    if form.is_valid():
        acc_resp = form.save()
        serializer = AccesibilitatRespiratoriaSerializer(acc_resp)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_accessibilitat_respiratoria(request, pk):
    accessibility = get_object_or_404(AccesibilitatRespiratoria, pk=pk)
    serializer = AccesibilitatRespiratoriaSerializer(accessibility, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_accessibilitat_respiratoria(request, pk):
    accessibility = get_object_or_404(AccesibilitatRespiratoria, pk=pk)
    if accessibility is not None:
        accessibility.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)

# LA PART DE USUARI ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_usuaris(request):
    usuaris = Usuari.objects.all()
    serializer = UsuariSerializer(usuaris, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_usuari(request, pk):
    usuari = get_object_or_404(Usuari, pk=pk)
    serializer = UsuariSerializer(usuari)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_usuari(request):
    data = {
        'correu': request.data.get('correu'),
        'password': request.data.get('password'),
        'nom': request.data.get('nom'),
        'estat': request.data.get('estat', "actiu"),
        'punts': request.data.get('punts', 0),
        'deshabilitador': request.data.get('deshabilitador', None),
        'about': request.data.get('about', None)
    }
    form = UsuariForm(data=data)
    if form.is_valid():
        usuari = form.save()
        serializer = UsuariSerializer(usuari)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_usuari(request):
    correu = request.data.get('correu')
    password = request.data.get('password')

    try:
        usuari = Usuari.objects.get(correu=correu)
        if usuari.deshabilitador is not None: # si el usuari esta deshabilitat, no pot fer login.
            return Response({'error': 'Usuari deshabilitat'}, status=status.HTTP_401_UNAUTHORIZED)
        if usuari.password == password:  # Cal modificar per que es fagi amb un hash
            serializer = UsuariSerializer(usuari)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except Usuari.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH'])
def update_usuari(request, pk):
    usuari = get_object_or_404(Usuari, pk=pk)
    serializer = UsuariSerializer(usuari, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_usuari(request, pk):
    usuari = get_object_or_404(Usuari, pk=pk)
    if usuari is not None:
        usuari.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH', 'PUT', 'POST'])
def deshabilitar_usuari(request, correu_deshabilitador, correu_usuari):
    deshabilitador = get_object_or_404(Admin, correu=correu_deshabilitador)
    usuari_a_deshabilitar = get_object_or_404(Usuari, correu=correu_usuari)
    usuari_a_deshabilitar.deshabilitador = deshabilitador
    usuari_a_deshabilitar.estat = "inactiu"
    usuari_a_deshabilitar.save()
    return Response(status=status.HTTP_200_OK)

@api_view(['PATCH', 'PUT', 'POST'])
def rehabilitar_usuari(request, correu_usuari):
    usuari_a_rehabilitar = get_object_or_404(Usuari, correu=correu_usuari)
    usuari_a_rehabilitar.deshabilitador = None
    usuari_a_rehabilitar.estat = "actiu"
    usuari_a_rehabilitar.save()
    return Response(status=status.HTTP_200_OK)

# LA PART DE ADMIN ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_admins(request):
    admins = Admin.objects.all()
    serializer = AdminSerializer(admins, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_admin(request, pk):
    admin = get_object_or_404(Admin, pk=pk)
    serializer = AdminSerializer(admin)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_admin(request):
    data = {
        'correu': request.data.get('correu'),
        'password': request.data.get('password'),
        'nom': request.data.get('nom'),
        'estat': request.data.get('estat', "actiu"),
        'punts': request.data.get('punts', 0),
        'deshabilitador': request.data.get('deshabilitador', None),
        'about': request.data.get('about', None)
    }
    form = AdminForm(data=data)
    if form.is_valid():
        admin = form.save()
        serializer = AdminSerializer(admin)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_admin(request, pk):
    admin = get_object_or_404(Admin, pk=pk)
    serializer = AdminSerializer(admin, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['DELETE'])
def delete_admin(request, pk):
    admin = get_object_or_404(Admin, pk=pk)
    if admin is not None:
        admin.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)

# LA PART DE BLOQUEI ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_bloqueigs(request):
    bloqueigs = Bloqueig.objects.all()
    serializer = BloqueigSerializer(bloqueigs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_bloqueig(request, pk):
    bloqueig = get_object_or_404(Bloqueig, pk=pk)
    serializer = BloqueigSerializer(bloqueig)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_bloqueig(request):
    data = {
        'bloqueja': request.data.get('bloqueja'),
        'bloquejat': request.data.get('bloquejat')
    }
    possible_amistat = Amistat.objects.filter(Q(solicita=data.get('bloqueja')) & Q(accepta=data.get('bloquejat')) | Q(solicita=data.get('bloquejat')) & Q(accepta=data.get('bloqueja')))
    if possible_amistat.exists():
        possible_amistat.delete()
    form = BloqueigForm(data=data)
    if form.is_valid():
        bloqueig = form.save()
        serializer = BloqueigSerializer(bloqueig)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_bloqueig(request, pk):
    bloqueig = get_object_or_404(Bloqueig, pk=pk)
    serializer = BloqueigSerializer(bloqueig, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_bloqueig(request, pk):
    bloqueig = get_object_or_404(Bloqueig, pk=pk)
    if bloqueig is not None:
        bloqueig.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)

# LA PART DE AMISTAT ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_amistats(request):
    amistats = Amistat.objects.all()
    serializer = AmistatSerializer(amistats, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_amistat(request, pk):
    amistat = get_object_or_404(Amistat, pk=pk)
    serializer = AmistatSerializer(amistat)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_amistat(request):
    data = {
        'solicita': request.data.get('solicita'),
        'accepta': request.data.get('accepta'),
        'pendent': request.data.get('pendent', True)
    }
    form = AmistatForm(data=data)
    if form.is_valid():
        amistat = form.save()
        serializer = AmistatSerializer(amistat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_amistat(request, pk):
    amistat = get_object_or_404(Amistat, pk=pk)
    serializer = AmistatSerializer(amistat, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_amistat(request, pk):
    amistat = get_object_or_404(Amistat, pk=pk)
    if amistat is not None:
        amistat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_amics_usuari(request, pk):
    usuari = get_object_or_404(Usuari, correu=pk)
    llistat_retorn = []
    amics = Amistat.objects.filter((Q(solicita=usuari) | Q(accepta=usuari)) & Q(pendent=False))
    for amic in amics:
        if amic.solicita == usuari:
            llistat_retorn.append({
                'correu': amic.accepta.correu,
                'nom': amic.accepta.nom,
                'punts': amic.accepta.punts,
                'about': amic.accepta.about
            })
        else:
            llistat_retorn.append({
                'correu': amic.solicita.correu,
                'nom': amic.solicita.nom,
                'punts': amic.solicita.punts,
                'about': amic.solicita.about
            })
    return Response(llistat_retorn, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_solicituds_rebudes(request, pk):
    usuari = get_object_or_404(Usuari, correu=pk)
    amics = Amistat.objects.filter(Q(accepta=usuari) & Q(pendent=True))
    serializer = AmistatSerializer(amics, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_solicituds_enviades(request, pk):
    usuari = get_object_or_404(Usuari, correu=pk)
    amics = Amistat.objects.filter(Q(solicita=usuari) & Q(pendent=True))
    serializer = AmistatSerializer(amics, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)





# LA PART DE RUTA ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_rutas(request):
    rutas = Ruta.objects.all()
    serializer = RutaSerializer(rutas, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_ruta(request, pk):
    ruta = get_object_or_404(Ruta, pk=pk)
    serializer = RutaSerializer(ruta)   
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_ruta(request):
    data = {
        'descripcio': request.data.get('descripcio'),
        'nom': request.data.get('nom'),
        'dist_km': request.data.get('dist_km')
    }
    form = RutaForm(data=data)
    if form.is_valid():
        ruta = form.save()
        serializer = RutaSerializer(ruta)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_ruta(request, pk):
    ruta = get_object_or_404(Ruta, pk=pk)
    serializer = RutaSerializer(ruta, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_ruta(request,pk):
    ruta = get_object_or_404(Ruta, pk=pk)
    if ruta is not None:
        ruta.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)

# LA PART DE VALORACIO ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_valoracions(request):
    valoracions = Valoracio.objects.all()
    serializer = ValoracioSerializer(valoracions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_valoracio(request,pk):
    valoracio = Valoracio.objects.get(pk=pk)
    serializer = ValoracioSerializer(valoracio)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_valoracio(request):
    data = {
        'usuari': request.data.get('usuari'),
        'ruta': request.data.get('ruta'),
        'puntuacio': request.data.get('puntuacio'),
        'comentari': request.data.get('comentari')
    }
    form = ValoracioForm(data=data)
    if form.is_valid():
        valoracio = form.save()
        serializer = ValoracioSerializer(valoracio)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_valoracio(request, pk):
    valoracio = get_object_or_404(Valoracio, pk=pk)
    serializer = ValoracioSerializer(valoracio, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_valoracio(request, pk):
    valoracio = get_object_or_404(Valoracio, pk=pk)
    if valoracio is not None:
        valoracio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)

# LA PART DE RECOMPENSA ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_recompenses(request):
    recompenses = Recompensa.objects.all()
    serializer = RecompensaSerializer(recompenses, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_recompensa(request, pk):
    recompensa = get_object_or_404(Recompensa, pk=pk)
    serializer = RecompensaSerializer(recompensa)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_recompensa(request):
    data = {
        'usuari': request.data.get('usuari'),
        'ruta': request.data.get('ruta'),
        'punts': request.data.get('punts'),
        'comentari': request.data.get('comentari')
    }
    form = RecompensaForm(data=data)
    if form.is_valid():
        recompensa = form.save()
        serializer = RecompensaSerializer(recompensa)
        usuari = get_object_or_404(Usuari, pk=request.data.get('usuari'))
        usuari.punts += recompensa.punts
        usuari.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_recompensa(request, pk):
    recompensa = get_object_or_404(Recompensa, pk=pk)
    serializer = RecompensaSerializer(recompensa, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        actualitza_recompensa_usuari(serializer.data.get('usuari'))
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_recompensa(request,pk):
    recompensa = get_object_or_404(Recompensa, pk=pk)
    if recompensa is not None:
        usuari = get_object_or_404(Usuari, pk=recompensa.usuari.pk)
        usuari.punts -= recompensa.punts
        usuari.save()
        recompensa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)

# LA PART DE ASSIGNACIO ESPORTIVA ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_assignacions_esportiva(request):
    assignacions = AssignaDificultatEsportiva.objects.all()
    serializer = AssignaDificultatEsportivaSerializer(assignacions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_assignacio_esportiva(request, pk):
    assignacio = get_object_or_404(AssignaDificultatEsportiva, pk=pk)
    serializer = AssignaDificultatEsportivaSerializer(assignacio)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_assignacio_esportiva(request):
    data = {
        'usuari': request.data.get('usuari'),
        'dificultat': request.data.get('dificultat'),
        'ruta': request.data.get('ruta')
    }
    form = AssignaDificultatEsportivaForm(data=data)
    if form.is_valid():
        assignacio = form.save()
        serializer = AssignaDificultatEsportivaSerializer(assignacio)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_assignacio_esportiva(request, pk):
    assignacio = get_object_or_404(AssignaDificultatEsportiva, pk=pk)
    serializer = AssignaDificultatEsportivaSerializer(assignacio, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_assignacio_esportiva(request, pk):
    assignacio = get_object_or_404(AssignaDificultatEsportiva, pk=pk)
    if assignacio is not None:
        assignacio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)

# LA PART DE ASSIGNACIO ACCESIBILITAT RESPIRATORIA ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_assignacions_accesibilitat_respiratoria(request):
    assignacions = AssignaAccesibilitatRespiratoria.objects.all()
    serializer = AssignaAccesibilitatRespiratoriaSerializer(assignacions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_assignacio_accesibilitat_respiratoria(request, pk):
    assignacio = get_object_or_404(AssignaAccesibilitatRespiratoria, pk=pk)
    serializer = AssignaAccesibilitatRespiratoriaSerializer(assignacio)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_assignacio_accesibilitat_respiratoria(request):
    data = {
        'usuari': request.data.get('usuari'),
        'ruta': request.data.get('ruta'),
        'accesibilitat': request.data.get('accesibilitat')
    }
    form = AssignaAccesibilitatRespiratoria(data = data)
    if form.is_valid():
        assignacio = form.save()
        serializer = AssignaAccesibilitatRespiratoriaSerializer(assignacio)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_assignacio_accesibilitat_respiratoria(request, pk):
    assignacio = get_object_or_404(AssignaAccesibilitatRespiratoria, pk=pk)
    serializer = AssignaAccesibilitatRespiratoriaSerializer(assignacio, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_assignacio_accesibilitat_respiratoria(request, pk):
    assignacio = get_object_or_404(AssignaAccesibilitatRespiratoria, pk=pk)
    if assignacio is not None:
        assignacio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)
    
# LA PART DE XAT ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_xats(request):
    xats = Xat.objects.all()
    serializer = XatSerializer(xats, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_xat(request, pk):
    xat = get_object_or_404(Xat, pk=pk)
    missatges_xat = Missatge.objects.filter(xat=xat)
    serializer_missatges = MissatgeSerializer(missatges_xat, many=True)
    serializer = XatSerializer(xat)
    return Response({'xat': serializer.data, 'missatges': serializer_missatges.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_xats_usuari(request, pk):
    usuari = get_object_or_404(Usuari, correu=pk)
    xats_individuals = XatIndividual.objects.filter(models.Q(usuari1=usuari) | models.Q(usuari2=usuari))
    data_xi = XatIndividualSerializer(xats_individuals, many=True)
    for dxi in data_xi.data:
        other_user = ""
        if dxi["usuari1"] == usuari.pk:
            other_user = get_object_or_404(Usuari, pk=dxi["usuari2"]).nom
        else:
            other_user = get_object_or_404(Usuari, pk=dxi["usuari1"]).nom
        dxi["nom"] = other_user
    xats_grupals = XatGrupal.objects.filter(membres=usuari)
    data_xg = XatGrupalSerializer(xats_grupals, many=True)
    data = data_xi.data + data_xg.data
    return Response(data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_xat(request):
    data = {
        'nom': request.data.get('nom')
    }
    form = XatForm(data=data)
    if form.is_valid():
        xat = form.save()
        serializer = XatSerializer(xat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_xat(request, pk):
    xat = get_object_or_404(Xat, pk=pk)
    serializer = XatSerializer(xat, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_xat(request, pk):
    xat = get_object_or_404(Xat, pk=pk)
    if xat is not None: 
        xat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)

# LA PART DE XAT INDIVIDUAL ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_xats_individual(request):
    xats_individual = XatIndividual.objects.all()
    serializer = XatIndividualSerializer(xats_individual, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_xat_individual(request, pk):
    xat_individual = get_object_or_404(XatIndividual, pk=pk)
    serializer = XatIndividualSerializer(xat_individual)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_xat_individual(request):
    data = {
        'nom': request.data.get('nom'),
        'usuari1': request.data.get('usuari1'),
        'usuari2': request.data.get('usuari2')
    }
    form = XatIndividualForm(data=data)
    if form.is_valid():
        xat_individual = form.save()
        serializer = XatIndividualSerializer(xat_individual)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_xat_individual(request, pk):
    xat_individual = get_object_or_404(XatIndividual, pk=pk)
    serializer = XatIndividualSerializer(xat_individual, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_xat_individual(request, pk):
    xat_individual = get_object_or_404(XatIndividual, pk=pk)
    if xat_individual is not None:
        xat_individual.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)

# LA PART DE XAT GRUPAL ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_xats_grupal(request):
    xats_grupal = XatGrupal.objects.all()
    serializer = XatGrupalSerializer(xats_grupal, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_xat_grupal(request, pk):
    xat_grupal = get_object_or_404(XatGrupal, pk=pk)
    serializer = XatGrupalSerializer(xat_grupal)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_xat_grupal(request):
    data = {
        'nom': request.data.get('nom'),
        'creador': request.data.get('creador'),
        'descripció': request.data.get('descripció'),
        'membres': request.data.get('membres')
    }
    form = XatGrupalForm(data=data)
    if form.is_valid():
        xat_grupal = form.save()
        serializer = XatGrupalSerializer(xat_grupal)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_xat_grupal(request, pk):
    xat_grupal = get_object_or_404(XatGrupal, pk=pk)
    serializer = XatGrupalSerializer(xat_grupal, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_xat_grupal(request, pk):
    xat_grupal = get_object_or_404(XatGrupal, pk=pk)
    if xat_grupal is not None:
        xat_grupal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PATCH', 'PUT', 'POST'])
def afegir_usuari_xat(request, pk, pkuser):
    xat = get_object_or_404(XatGrupal, pk=pk)
    usuari = get_object_or_404(Usuari, correu=pkuser)
    if not xat.membres.filter(pk=pkuser).exists():
        xat.membres.add(usuari)
        xat.save()
        return Response(status=status.HTTP_200_OK)
    return Response({'error': 'Usuari ja en el xat'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def eliminar_usuari_xat(request,pk,pkuser):
    xat = get_object_or_404(XatGrupal, pk=pk)
    usuari = get_object_or_404(Usuari, pk=pkuser)
    if xat.membres.filter(pk=pkuser).exists():
        xat.membres.remove(usuari)
        xat.save()
        return Response(status=status.HTTP_200_OK)
    return Response({'error': 'Usuari no en el xat'}, status=status.HTTP_400_BAD_REQUEST)
    
# LA PART DE INVITACIO ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_invitacions(request):
    invitacions = Invitacio.objects.all()
    serializer = InvitacioSerializer(invitacions, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_invitacio(request, pk):
    invitacio = get_object_or_404(Invitacio, pk=pk)
    serializer = InvitacioSerializer(invitacio)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_invitacio(request):
    data = {
        'destinatari': request.data.get('destinatari'),
        'creador': request.data.get('creador'),
        'estat': request.data.get('estat'),
        'xat': request.data.get('xat')
    }
    form = InvitacioForm(data=data)
    if form.is_valid():
        invitacio = form.save()
        serializer = InvitacioSerializer(invitacio)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_invitacio(request, pk):
    invitacio = get_object_or_404(Invitacio,pk=pk)
    serializer = InvitacioSerializer(invitacio, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_invitacio(request, pk):
    invitacio = get_object_or_404(Invitacio, pk=pk)
    if invitacio is not None: 
        invitacio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)

# LA PART DE MISSATGE ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_missatges(request):
    missatges = Missatge.objects.all()
    serializer = MissatgeSerializer(missatges, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_missatge(request, pk):
    missatge = get_object_or_404(Missatge, pk=pk)
    serializer = MissatgeSerializer(missatge)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_missatge(request):
    data = {
        'text': request.data.get('text'),
        'data': request.data.get('data', timezone.now()),
        'xat': request.data.get('xat'),
        'autor': request.data.get('autor')
    }
    form = MissatgeForm(data=data)
    if form.is_valid():
        missatge = form.save()
        serializer = MissatgeSerializer(missatge)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_missatge(request, pk):
    missatge = get_object_or_404(Missatge, pk=pk)
    serializer = MissatgeSerializer(missatge, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_missatge(request, pk):
    missatge = get_object_or_404(Missatge, pk=pk)
    if missatge is not None:
        missatge.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)
    
# LA PART DE EVENT DE CALENDARI ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_events_de_calendari(request):
    events_de_calendari = EventDeCalendari.objects.all()
    serializer = EventDeCalendariSerializer(events_de_calendari, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_event_de_calendari(request, pk):
    event_de_calendari = get_object_or_404(EventDeCalendari, pk=pk)
    serializer = EventDeCalendariSerializer(event_de_calendari)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_event_de_calendari(request):
    data ={
        'nom': request.data.get('nom'),
        'descripció': request.data.get('descripció'),
        'data_inici': request.data.get('data_inici', timezone.now()),
        'data_fi': request.data.get('data_fi', timezone.now()),
        'creador': request.data.get('creador')
    }
    form = EventDeCalendariForm(data=data)
    if form.is_valid():
        ev = form.save()
        serializer = EventDeCalendariSerializer(ev)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_event_de_calendari(request, pk):
    event_de_calendari = get_object_or_404(EventDeCalendari, pk=pk)
    serializer = EventDeCalendariSerializer(event_de_calendari, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_event_de_calendari(request, pk):
    event_de_calendari = get_object_or_404(EventDeCalendari, pk=pk)
    if event_de_calendari is not None:
        event_de_calendari.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)
    
# LA PART DE EVENT DE CALENDARI PRIVAT ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_events_de_calendari_privats(request):
    events_privats = EventDeCalendariPrivat.objects.all()
    serializer = EventDeCalendariPrivatSerializer(events_privats, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_event_de_calendari_privat(request, pk):
    event_privat = get_object_or_404(EventDeCalendariPrivat, pk=pk)
    serializer = EventDeCalendariPrivatSerializer(event_privat)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_event_de_calendari_privat(request):
    data = {
        'nom': request.data.get('nom'),
        'descripció': request.data.get('descripció'),
        'data_inici': request.data.get('data_inici', timezone.now()),
        'data_fi': request.data.get('data_fi', timezone.now()),
        'creador': request.data.get('creador'),
        'xat': request.data.get('xat')
    }
    form = EventDeCalendariPrivatForm(data=data)
    if form.is_valid():
        ev = form.save()
        serializer = EventDeCalendariPrivatSerializer(ev)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_event_de_calendari_privat(request, pk):
    event_privat = get_object_or_404(EventDeCalendariPrivat, pk=pk)
    serializer = EventDeCalendariPrivatSerializer(event_privat, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_event_de_calendari_privat(request, pk):
    event_privat = get_object_or_404(EventDeCalendariPrivat, pk=pk)
    if event_privat is not None:
        event_privat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)
    
# LA PART DE EVENT DE CALENDARI PUBLIC ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_events_de_calendari_publics(request):
    events_publics = EventDeCalendariPublic.objects.all()
    serializer = EventDeCalendariPublicSerializer(events_publics, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_event_de_calendari_public(request, pk):
    event_public = get_object_or_404(EventDeCalendariPublic, pk=pk)
    serializer = EventDeCalendariPublicSerializer(event_public)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_event_de_calendari_public(request):
    data = {
        'nom': request.data.get('nom'),
        'descripció': request.data.get('descripció'),
        'data_inici': request.data.get('data_inici', timezone.now()),
        'data_fi': request.data.get('data_fi', timezone.now()),
        'creador': request.data.get('creador'),
        'limit': request.data.get('limit')
    }
    form = EventDeCalendariPublicForm(data=data)
    if form.is_valid():
        ev = form.save()
        serializer = EventDeCalendariPublicSerializer(ev)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_event_de_calendari_public(request, pk):
    ev = get_object_or_404(EventDeCalendariPublic, pk=pk)
    serializer = EventDeCalendariPublicSerializer(ev, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_event_de_calendari_public(request, pk):
    event_public = get_object_or_404(EventDeCalendariPublic, pk=pk)
    if event_public is not None:
        event_public.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)
    
# LA PART DE APUNTAT ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_apuntats(request):
    apuntats = Apuntat.objects.all()
    serializer = ApuntatSerializer(apuntats, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_apuntat(request, pk):
    apuntat = get_object_or_404(Apuntat, pk=pk)
    serializer = ApuntatSerializer(apuntat)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_apuntat(request):
    data = {
        'event': request.data.get('event'),
        'usuari': request.data.get('usuari')
    }
    form = ApuntatForm(data=data)
    if form.is_valid():
        apuntat = form.save()
        serializer = ApuntatSerializer(apuntat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_apuntat(request, pk):
    apuntat = get_object_or_404(Apuntat, pk=pk)
    serializer = ApuntatSerializer(apuntat, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_apuntat(request, pk):
    apuntat = get_object_or_404(Apuntat, pk=pk)
    if apuntat is not None:
        apuntat.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# LA PART DE PUNT ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_punts(request):
    punts = Punt.objects.all()
    serializer = PuntSerializer(punts, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_punt(request, pk):
    punt =  get_object_or_404(Punt, pk=pk)
    serializer = PuntSerializer(punt)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_punt(request):
    data = {
        'latitud': request.data.get('latitud'),
        'longitud': request.data.get('longitud'),
        'altitud': request.data.get('altitud'),
        'index_qualitat_aire': request.data.get('index_qualitat_aire')
    }
    form = PuntForm(data=data)
    if form.is_valid():
        punt = form.save()
        serializer = PuntSerializer(punt)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_punt(request, pk):
    punt = get_object_or_404(Punt, pk=pk)  
    serializer = PuntSerializer(punt, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_punt(request, pk):
    punt = get_object_or_404(Punt, pk=pk)
    if punt is not None:
        punt.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)
    
# LA PART DE ESTACIO QUALITAT AIRE ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_estacions_qualitat_aire(request):
    estacions_qualitat_aire = EstacioQualitatAire.objects.all()
    serializer = EstacioQualitatAireSerializer(estacions_qualitat_aire, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_estacio_qualitat_aire(request, pk):
    estacio_qualitat_aire = get_object_or_404(EstacioQualitatAire, pk=pk)
    serializer = EstacioQualitatAireSerializer(estacio_qualitat_aire)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_estacio_qualitat_aire(request):
    data = {
        'nom_estacio': request.data.get('nom_estacio'),
        'descripcio': request.data.get('descripcio'),
        'latitud': request.data.get('latitud'),
        'longitud': request.data.get('longitud'),
        'altitud': request.data.get('altitud'),
        'index_qualitat_aire': request.data.get('index_qualitat_aire')
    }
    form = EstacioQualitatAireForm(data=data)
    if form.is_valid():
        estacio = form.save()
        serializer = EstacioQualitatAireSerializer(estacio)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['PATCH'])
def update_estacio_qualitat_aire(request, pk):
    estacio_qualitat_aire = get_object_or_404(EstacioQualitatAire, pk=pk)
    serializer = EstacioQualitatAireSerializer(estacio_qualitat_aire, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK) 
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_estacio_qualitat_aire(request, pk):
    estacio_qualitat_aire = get_object_or_404(EstacioQualitatAire, pk=pk)
    if estacio_qualitat_aire is not None:
        estacio_qualitat_aire.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)
        
# LA PART DE ACTIVITAT CULTURAL ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_activitats_culturals(request):
    activitats_culturals = ActivitatCultural.objects.all()
    serializer = ActivitatCulturalSerializer(activitats_culturals, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_activitat_cultural(request, pk):
    activitat_cultural = get_object_or_404(ActivitatCultural, pk=pk)
    serializer = ActivitatCulturalSerializer(activitat_cultural)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_activitat_cultural(request):
    data = {
        'nom_activitat': request.data.get('nom_activitat'),
        'descripcio': request.data.get('descripcio'),
        'data_inici': request.data.get('data_inici'),
        'data_fi': request.data.get('data_fi'),
    }
    form = ActivitatCulturalForm(data=data)
    if form.is_valid():
        activitat = form.save()
        serializer = ActivitatCulturalSerializer(activitat)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_activitat_cultural(request, pk):
    activitat_cultural = get_object_or_404(ActivitatCultural, pk=pk)
    serializer = ActivitatCulturalSerializer(activitat_cultural, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_activitat_cultural(request, pk):
    activitat_cultural = get_object_or_404(ActivitatCultural, pk=pk)
    if activitat_cultural is not None:
        activitat_cultural.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)

# LA PART DE CONTAMINANT ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_contaminants(request):
    contaminants = Contaminant.objects.all()
    serializer = ContaminantSerializer(contaminants, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_contaminant(request, pk):
    contaminant = get_object_or_404(Contaminant, pk=pk)
    serializer = ContaminantSerializer(contaminant)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_contaminant(request):
    data = {
        'nom': request.data.get('nom'),
        'informacio': request.data.get('informacio')
    }
    form = ContaminantForm(data=data)
    if form.is_valid():
        contaminant = form.save()
        serializer = ContaminantSerializer(contaminant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_contaminant(request, pk):
    contaminant = get_object_or_404(Contaminant, pk=pk)
    serializer = ContaminantSerializer(contaminant, data = request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_contaminant(request, pk):
    contaminant = get_object_or_404(Contaminant, pk=pk)
    if contaminant is not None:
        contaminant.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)
    
# LA PART DE PRESENCIA ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def get_presencies(request):
    presencies = Presencia.objects.all()
    resultats = []
    contaminants = ['NO2','O3','PM10','H2S', 'NO', 'SO2', 'PM2.5', 'NOX', 'CO', 'C6H6', 'PM1', 'Hg']
    mapa_contaminants = {
        'NO2': 2,
        'O3': 3,
        'PM10': 4,
        'H2S': 41091,
        'NO': 41092,
        'SO2': 41093,
        'PM2.5': 41096,
        'NOX': 41097,
        'CO': 41098,
        'C6H6': 41100,
        'PM1': 41101,
        'Hg': 41102
    }
    for nom in contaminants:
        if request.query_params.get(nom):
            valor  = mapa_contaminants[nom]
            resultats.append(valor) # basicament el que fem es anar adjuntant la llista de contaminants que hi ha en el request, perquè filtren.
    
    resultat_final = presencies
    if resultats:
        resultat_final = resultat_final.filter(contaminant_id__in=resultats) 
    serializer = PresenciaSerializer(resultat_final, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_presencia(request,pk):
    presencia = get_object_or_404(Presencia, pk=pk)
    contaminants = ['NO2','O3','PM10','H2S', 'NO', 'SO2', 'PM2.5', 'NOX', 'CO', 'C6H6', 'PM1', 'Hg']
    mapa_contaminants = {
        'NO2': 2,
        'O3': 3,
        'PM10': 4,
        'H2S': 41091,
        'NO': 41092,
        'SO2': 41093,
        'PM2.5': 41096,
        'NOX': 41097,
        'CO': 41098,
        'C6H6': 41100,
        'PM1': 41101,
        'Hg': 41102
    }
    resultats = []
    for nom in contaminants:
        if request.query_params.get(nom):
            valor = mapa_contaminants[nom]
            resultats.append(valor)
            
    resultat_final = presencia
    if resultats:
        resultat_final= resultat_final.filter(contaminant_id__in=resultats)
 
    serializer = PresenciaSerializer(resultat_final)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def create_presencia(request):
    data={
        'punt': request.data.get('punt'),
        'contaminant': request.data.get('contaminant'),
        'data': request.data.get('data', timezone.now()),
        'valor': request.data.get('valor')
    }
    form = PresenciaForm(data=data)
    if form.is_valid():
        presencia = form.save()
        serializer = PresenciaSerializer(presencia)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_presencia(request, pk):
    presencia = get_object_or_404(Presencia, pk=pk)
    serializer = PresenciaSerializer(presencia, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_presencia(request, pk):
    presencia = get_object_or_404(Presencia, pk=pk)
    if presencia is not None:
        presencia.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_presencies_punt(request, pk):
    punt = get_object_or_404(Punt, pk=pk)
    if punt is not None:
        contaminants = ['NO2','O3','PM10','H2S', 'NO', 'SO2', 'PM2.5', 'NOX', 'CO', 'C6H6', 'PM1', 'Hg']
        mapa_contaminants = {
            'NO2': 2,
            'O3': 3,
            'PM10': 4,
            'H2S': 41091,
            'NO': 41092,
            'SO2': 41093,
            'PM2.5': 41096,
            'NOX': 41097,
            'CO': 41098,
            'C6H6': 41100,
            'PM1': 41101,
            'Hg': 41102
        }
        presencies = Presencia.objects.filter(punt=punt.id)
        resultats = []
        for nom in contaminants:
            if request.query_params.get(nom):
                valor = mapa_contaminants[nom]
                resultats.append(valor)
        resultat_final = presencies
        if resultats:
            resultat_final = resultat_final.filter(contaminant_id__in=resultats)
        
        serializer = PresenciaSerializer(resultat_final, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_presencies_punt_lon_lat(request, lon, lat):
    punt = Punt.objects.filter(longitud=lon, latitud=lat)
    if punt is not None:
        presencies = Presencia.objects.filter(punt=punt.id)
        serializer = PresenciaSerializer(presencies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)
    
# LA PART DE DADES OBERTES ------------------------------------------------------------------------------------------------

@api_view(['GET'])
def actualitzar_rutes_manualment(request):
    actualitzar_rutes()
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def actualitzar_estacions_qualitat_aire_manualment(request):
    actualitzar_estacions_qualitat_aire()
    return Response(status=status.HTTP_200_OK)

@api_view(['GET'])
def actualitzar_activitats_culturals_manualment(request):
    actualitzar_activitats_culturals()
    return Response(status=status.HTTP_200_OK)

#------------------------------------------  RANKING ---------------------------------

@api_view(['GET'])
def obtenir_ranking_usuaris_all(request):
    usuaris = Usuari.objects.all().order_by('-punts')
    serializer = UsuariSerializer(usuaris, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def obtenir_ranking_usuari_amics(request, pk):
    usuari = get_object_or_404(Usuari, correu=pk)
    llistat_amics = Amistat.objects.filter(Q(solicita=usuari) | Q(accepta=usuari))
    amics = []
    amics.append(usuari)
    for amistat in llistat_amics:
        if amistat.solicita == usuari:
            amics.append(amistat.accepta)
        else:
            amics.append(amistat.solicita)
    rank = Usuari.objects.filter(correu__in=[u.correu for u in amics]).order_by('-punts')
    serializer = UsuariSerializer(rank, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
#------------------------------------------  NORMALITZACIO ---------------------------------

@api_view(['GET'])
def normalitzar_valor_contaminant(request, pk):
    presencia = get_object_or_404(Presencia, pk=pk)
    contaminant = get_object_or_404(Contaminant, pk=presencia.contaminant.id)
    index_qca = get_object_or_404(IndexQualitatAire, contaminant=contaminant)
    valor_normalitzat = index_qca.normalitzar_valor(presencia.valor)
    return Response({'contaminant': contaminant.nom, 'valor_normalitzat': valor_normalitzat}, status=status.HTTP_200_OK)

@api_view(['GET'])
def normalitzar_valor_contaminant_punt(request, pk):
    punt = get_object_or_404(Punt, pk=pk)
    presencies = Presencia.objects.filter(punt=punt)
    llista_normalitzada = []
    for presencia in presencies:
        contaminant = get_object_or_404(Contaminant, pk=presencia.contaminant.id)
        index_qca = get_object_or_404(IndexQualitatAire, contaminant=contaminant)
        valor_normalitzat = index_qca.normalitzar_valor(presencia.valor)
        llista_normalitzada.append({'contaminant': contaminant.nom, 'valor_normalitzat': valor_normalitzat})
    return Response(llista_normalitzada, status=status.HTTP_200_OK)
    
    
#------------------------------------------  INDEX QUALITAT DE L'AIRE TAULA 
# 
# ---------------------------------

@api_view(['GET'])
def get_index_qualitat_aire_taula(request):
    index_qca = IndexQualitatAire.objects.all()
    serializer = IndexQualitatAireSerializer(index_qca, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_index_qualitat_aire_taula_contaminant(request, pk):
    contaminant = get_object_or_404(Contaminant, pk=pk)
    index_qca = IndexQualitatAire.objects.filter(contaminant=contaminant)
    serializer = IndexQualitatAireSerializer(index_qca, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_index_qualitat_aire_taula(request):
    data = {
        'contaminant': request.data.get('contaminant'),
        'valors_intervals': request.data.get('valors_intervals')
    }
    form = IndexQualitatAireForm(data=data)
    if form.is_valid():
        index_qca = form.save()
        serializer = IndexQualitatAireSerializer(index_qca)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_index_qualitat_aire_taula(request, pk):
    index_qca = get_object_or_404(IndexQualitatAire, contaminant=pk)
    serializer = IndexQualitatAireSerializer(index_qca, data=request.data, partial=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_index_qualitat_aire_taula(request, pk):
    index_qca = get_object_or_404(IndexQualitatAire, contaminant=pk)
    index_qca.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

