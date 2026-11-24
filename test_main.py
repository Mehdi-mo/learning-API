from fastapi.testclient import TestClient
from part11_model_api import app

def test_health():
    with TestClient(app) as client:
        r = client.get('/health')
        assert r.status_code == 200
        assert r.json()['status'] == "ok"

def test_predict_good_input():
    with TestClient(app) as client:
        student = {"hours_studied": 10, "attendance":50}
        r = client.post('/predict', json = student)
        assert r.status_code == 200
        assert 0 <= r.json()["pass_probability"] <= 1

def test_predict_bad_input():
    with TestClient(app) as client:
        r = client.post('/predict', json={"hours_studied": -5, "attendance": 50})
        assert r.status_code == 422


