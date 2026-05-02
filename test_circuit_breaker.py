import pytest
from fastapi.testclient import TestClient
from main import app, cb

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_circuit_breaker():
    cb.failure_count = 0
    cb.last_failure_time = None
    cb.state = "CLOSED"
    yield

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_student_id_header_present():
    response = client.get("/health")
    assert "x-student-id" in response.headers
    assert response.headers["x-student-id"] == "23049"

def test_fallback_when_llm_is_down():
    response = client.get("/ask")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "fallback"
    assert "temporarily unavailable" in data["response"]

def test_circuit_opens_after_threshold():
    for i in range(3):
        client.get("/ask")
    response = client.get("/circuit-status")
    data = response.json()
    assert data["state"] == "OPEN"
    assert data["failure_count"] >= 3

def test_open_circuit_returns_open_reason():
    for i in range(3):
        client.get("/ask")
    response = client.get("/ask")
    data = response.json()
    assert data["status"] == "fallback"

def test_circuit_status_endpoint():
    response = client.get("/circuit-status")
    assert response.status_code == 200
    data = response.json()
    assert "state" in data
    assert "failure_count" in data
    assert data["state"] == "CLOSED"
