import pytest
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from .models import User, Empresa, Comentario, Ticket

@pytest.fixture
def cria_empresa():
    name = "A.C.M.E"
    empresa = Empresa.objects.create(name=name)
    return empresa

@pytest.fixture
def cria_usuario(cria_empresa):
    username = "foo"
    password = "bar"
    user = User.objects.create(
        username=username, password=password, empresa=cria_empresa
    )
    return user

@pytest.fixture
def cliente_autenticado(cria_usuario):
    token = Token.objects.get(user__username="foo")
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")
    return client

@pytest.fixture
def cliente_nao_autenticado():
    client = APIClient()
    return client

# Create your tests here.
def test_pytest_roda():
    assert True

@pytest.mark.django_db
def test_consegue_ver_ticket(cliente_autenticado):
    client = cliente_autenticado
    response = client.get("/ticket/")
    assert response.status_code == 200

@pytest.mark.django_db
def test_nao_consegue_ver_ticket(cliente_nao_autenticado):
    client = cliente_nao_autenticado
    response = client.get("/ticket/")
    assert response.status_code == 401
