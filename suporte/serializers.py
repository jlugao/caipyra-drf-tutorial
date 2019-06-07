from rest_framework import serializers
from .models import Empresa, User, Ticket, Comentario


class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Empresa
        exclude=("id",)

class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "empresa")

class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = "__all__"

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = "__all__"
