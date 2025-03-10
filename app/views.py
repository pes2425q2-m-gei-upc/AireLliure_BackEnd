from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from .forms import *
from django.shortcuts import get_object_or_404
from rest_framework import status



# LA PART DE CATEGORIA

@api_view(['GET'])
def get_categories(request):
    dificultats = DificultatEsportiva.objects.all()
    accessibilitats = AccesibilitatRespiratoria.objects.all()
    #Agafem totes i el que fem ara a continuacio es les postejem.
    dificultats = DificultatEsportivaSerializer(dificultats, many=True)
    accessibilitats = AccesibilitatRespiratoriaSerializer(accessibilitats, many=True)
    return Response({
        'dificultats': dificultats.data,
        'accessibilitats': accessibilitats.data
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_category(request, pk):
    try:
        category = DificultatEsportiva.objects.get(nombre=pk)
    except DificultatEsportiva.DoesNotExist:
        try:
            category = AccesibilitatRespiratoria.objects.get(nombre=pk)
        except AccesibilitatRespiratoria.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = CategoriaSerializer(category)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_category(request, pk):
    try:
        category = DificultatEsportiva.objects.get(nombre=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except DificultatEsportiva.DoesNotExist:
        try:
            category = AccesibilitatRespiratoria.objects.get(nombre=pk)
            category.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AccesibilitatRespiratoria.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

#Dificultat Esportiva
