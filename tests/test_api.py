# tests/test_api.py
def test_create_product(client):
    response = client.post("/api/products/", json={"url": "https://example.com/product/1",  "name": "Тестовый товар"})
    assert response.status_code == 200

    data = response.json()
    assert data["url"] == "https://example.com/product/1"
    assert data["name"] == "Тестовый товар"
    assert data["current_price"] == 999.99
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_read_product(client):
    # Сначала создаём
    create_response = client.post("/api/products/", json={"url": "https://example.com/product/2",  "name": "Второй товар"})

    product_id = create_response.json()["id"]

    # Потом читаем
    response = client.get(f"/api/products/{product_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == product_id
    assert data["url"] == "https://example.com/product/2"
    assert data["name"] == "Второй товар"