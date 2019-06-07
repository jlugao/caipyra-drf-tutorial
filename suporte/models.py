from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
# http://t.me/caipyra
# https://github.com/jlugao/drf-example


class Empresa(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nome")

    def __str__(self):
        return self.name

class User(AbstractUser):
    empresa = models.ForeignKey(
        "suporte.Empresa",
        related_name="usuarios",
        on_delete=models.CASCADE,
        blank=True, null=True
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

@receiver(post_save, sender=User)
def create_user_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Ticket(models.Model):
    CHOICES_STATUS = (
        ("A","Aguardando Resposta"),
        ("V","Visualizado"),
        ("R","Respondido")
    )
    status = models.CharField(max_length=1, choices=CHOICES_STATUS)
    empresa = models.ForeignKey(
        "suporte.Empresa",
        related_name="tickets",
        on_delete=models.CASCADE,
        blank=True, null=True
    )
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(max_length=700)
    def __str__(self):
        return self.titulo + " - " + self.status

class Comentario(models.Model):
    ticket = models.ForeignKey("suporte.ticket", related_name="comentarios", on_delete=models.CASCADE)
    user = models.ForeignKey("suporte.user", related_name="comentarios", on_delete=models.CASCADE)
    texto = models.TextField(max_length=500)
