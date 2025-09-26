import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


def test_list_machines(client: TestClient):
    """Test listing all machines"""
    response = client.get("/machines/")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0  # Should have seeded machines


def test_get_machine(client: TestClient, db_session: Session):
    """Test getting a machine by ID"""
    # Get first machine from seeded data
    from app.models.machine import Machine
    machine = db_session.query(Machine).first()
    assert machine is not None
    
    response = client.get(f"/machines/{machine.id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == machine.id
    assert data["name"] == machine.name


def test_create_machine(client: TestClient):
    """Test creating a new machine"""
    machine_data = {
        "name": "test_machine",
        "cpu": "Intel i7",
        "gpu": "RTX 3080",
        "memory": 32.0,
        "status": "available"
    }
    
    response = client.post("/machines/", json=machine_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == "test_machine"
    assert data["cpu"] == "Intel i7"
    assert data["gpu"] == "RTX 3080"
    assert data["memory"] == 32.0


def test_update_machine_status(client: TestClient, db_session: Session):
    """Test updating machine status"""
    from app.models.machine import Machine
    machine = db_session.query(Machine).first()
    
    response = client.patch(f"/machines/{machine.id}/status?status=busy")
    assert response.status_code == 200
    
    data = response.json()
    assert "status updated to busy" in data["message"]


def test_machine_not_found(client: TestClient):
    """Test getting non-existent machine"""
    response = client.get("/machines/99999")
    assert response.status_code == 404
