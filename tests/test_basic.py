# Teste básico para aplicação Flask
import pytest
from main import app

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Login" in response.data  # Verifica se o título da página está presente
