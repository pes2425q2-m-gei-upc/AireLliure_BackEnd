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



# LA PART DE CATEGORIA
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
        'estat': request.data.get('estat'),
        'punts': request.data.get('punts', 0),
        'deshabilitador': request.data.get('deshabilitador', None)
    }
    form = UsuariForm(data=data)
    if form.is_valid():
        usuari = form.save()
        serializer = UsuariSerializer(usuari)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

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
        'estat': request.data.get('estat'),
        'punts': request.data.get('punts', 0),
        'deshabilitador': request.data.get('deshabilitador', None)
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
        'accepta': request.data.get('accepta')
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
        'puntuacio': request.data.get('puntuacio'),
        'comentari': request.data.get('comentari')
    }
    form = RecompensaForm(data=data)
    if form.is_valid():
        recompensa = form.save()
        serializer = RecompensaSerializer(recompensa)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH'])
def update_recompensa(request, pk):
    recompensa = get_object_or_404(Recompensa, pk=pk)
    serializer = RecompensaSerializer(recompensa, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_recompensa(request,pk):
    recompensa = get_object_or_404(Recompensa, pk=pk)
    if recompensa is not None:
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
    serializer = XatSerializer(xat)
    return Response(serializer.data, status=status.HTTP_200_OK)

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
        'nom': request.data.get('nom')
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
        'descripció': request.data.get('descripció'),
        'creador': request.data.get('creador'),
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

# LA PART DE EVENT DE CALENDARI PRIVAT ------------------------------------------------------------------------------------------------

# LA PART DE EVENT DE CALENDARI PUBLIC ------------------------------------------------------------------------------------------------

# LA PART DE APUNTAT ------------------------------------------------------------------------------------------------

# LA PART DE PUNT ------------------------------------------------------------------------------------------------

# LA PART DE ESTACIO QUALITAT AIRE ------------------------------------------------------------------------------------------------

# LA PART DE ACTIVITAT CULTURAL ------------------------------------------------------------------------------------------------

# LA PART DE CONTAMINANT ------------------------------------------------------------------------------------------------

# LA PART DE PRESENCIA ------------------------------------------------------------------------------------------------
