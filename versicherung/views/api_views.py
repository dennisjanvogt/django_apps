from ..models import Mitarbeiter, Kunde, Schadensfall, Versicherungsvertrag

from ..serializers import (
    KundeSerializer,
    VersicherungsvertragSerializer,
    SchadensfallSerializer,
    MitarbeiterSerializer,
)
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def mitarbeiter_list_create(request):
    if request.method == "GET":
        mitarbeiter = Mitarbeiter.objects.all()
        serializer = MitarbeiterSerializer(mitarbeiter, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = MitarbeiterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def mitarbeiter_retrieve_update_destroy(request, pk):
    try:
        mitarbeiter = Mitarbeiter.objects.get(pk=pk)
    except Mitarbeiter.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = MitarbeiterSerializer(mitarbeiter)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = MitarbeiterSerializer(mitarbeiter, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        mitarbeiter.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def kunde_list_create(request):
    if request.method == "GET":
        kunden = Kunde.objects.all()
        serializer = KundeSerializer(kunden, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = KundeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def kunde_retrieve_update_destroy(request, pk):
    try:
        kunde = Kunde.objects.get(pk=pk)
    except Kunde.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = KundeSerializer(kunde)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = KundeSerializer(kunde, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        kunde.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def versicherungsvertrag_list_create(request):
    if request.method == "GET":
        vertraege = Versicherungsvertrag.objects.all()
        serializer = VersicherungsvertragSerializer(vertraege, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = VersicherungsvertragSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def versicherungsvertrag_retrieve_update_destroy(request, pk):
    try:
        vertrag = Versicherungsvertrag.objects.get(pk=pk)
    except Versicherungsvertrag.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = VersicherungsvertragSerializer(vertrag)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = VersicherungsvertragSerializer(vertrag, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        vertrag.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def schaden_list_create(request):
    if request.method == "GET":
        schaeden = Schadensfall.objects.all()
        serializer = SchadensfallSerializer(schaeden, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = SchadensfallSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated])
def schaden_retrieve_update_destroy(request, pk):
    try:
        schaden = Schadensfall.objects.get(pk=pk)
    except Schadensfall.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == "GET":
        serializer = SchadensfallSerializer(schaden)
        return Response(serializer.data)
    elif request.method == "PUT":
        serializer = SchadensfallSerializer(schaden, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        schaden.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
