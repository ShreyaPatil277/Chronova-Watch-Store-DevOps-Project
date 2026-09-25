import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    res = client.get("/")
    assert res.status_code == 200

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200

def test_list_watches(client):
    res = client.get("/watches")
    assert res.status_code == 200
    assert len(res.get_json()) >= 1

def test_add_watch_and_order(client):
    res = client.post("/watches", json={"name": "Solstice Gold", "brand": "Chronova", "price": 299.0})
    assert res.status_code == 201
    watches = client.get("/watches").get_json()
    new_watch = [w for w in watches if w["name"] == "Solstice Gold"][0]
    res = client.post("/orders", json={"watch_id": new_watch["id"], "customer_name": "Test User"})
    assert res.status_code == 201
