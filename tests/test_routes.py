def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"login" in response.data  # Ajuste conforme o conteúdo do template
