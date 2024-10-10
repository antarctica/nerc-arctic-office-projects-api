def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200


def test_health_check_route(client):
    response = client.get("/meta/health/canary")
    assert response.status_code == 204
