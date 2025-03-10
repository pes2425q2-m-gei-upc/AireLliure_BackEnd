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

