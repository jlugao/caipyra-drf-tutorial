from django.shortcuts import render
from rest_framework import viewsets
# Create your views here.

from .models import Empresa, User, Ticket, Comentario
from .serializers import EmpresaSerializer, UserSerializer, TicketSerializer, ComentarioSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters import rest_framework as filters

class EmpresaViewSet(viewsets.ModelViewSet):
    serializer_class = EmpresaSerializer
    queryset = Empresa.objects.all()

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()
    filter_backends=(filters.DjangoFilterBackend,)
    filterset_fields = ("status", "empresa")

    @action(detail=True, methods=["get"])
    def comentarios(self, request, pk=None):
        queryset = Comentario.objects.filter(ticket__id=pk)
        serializer = ComentarioSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def adicionar_comentario(self, request, pk=None):
        user = request.user
        form_comentario = request.data
        form_comentario["user"] = user.id
        form_comentario["ticket"] = pk
        serializer = ComentarioSerializer(data=form_comentario)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ComentarioViewSet(viewsets.ModelViewSet):
    serializer_class = ComentarioSerializer
    queryset = Comentario.objects.all()
