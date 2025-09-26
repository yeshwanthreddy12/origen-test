import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.simulation import Simulation, SimulationStatus
from app.models.machine import Machine
from app.schemas.simulation import SimulationCreate


def test_create_simulation(client: TestClient, db_session: Session):
    """Test creating a simulation"""
    # Get a machine first
    machine = db_session.query(Machine).first()
    assert machine is not None
    
    simulation_data = {
        "name": "test_simulation",
        "machine_id": machine.id
    }
    
    response = client.post("/simulations/", json=simulation_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == "test_simulation"
    assert data["machine_id"] == machine.id
    assert data["status"] == "pending"


def test_get_simulation(client: TestClient, db_session: Session):
    """Test getting a simulation by ID"""
    # Create a simulation first
    machine = db_session.query(Machine).first()
    simulation = Simulation(name="test_sim", machine_id=machine.id)
    db_session.add(simulation)
    db_session.commit()
    db_session.refresh(simulation)
    
    response = client.get(f"/simulations/{simulation.id}")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == simulation.id
    assert data["name"] == "test_sim"


def test_list_simulations(client: TestClient, db_session: Session):
    """Test listing simulations"""
    response = client.get("/simulations/")
    assert response.status_code == 200
    
    data = response.json()
    assert "simulations" in data
    assert "total" in data
    assert "page" in data
    assert "size" in data


def test_list_simulations_with_filter(client: TestClient, db_session: Session):
    """Test listing simulations with status filter"""
    response = client.get("/simulations/?status=pending")
    assert response.status_code == 200
    
    data = response.json()
    assert "simulations" in data


def test_get_simulation_detailed(client: TestClient, db_session: Session):
    """Test getting simulation with machine details using bare SQL"""
    # Create a simulation first
    machine = db_session.query(Machine).first()
    simulation = Simulation(name="test_sim_detailed", machine_id=machine.id)
    db_session.add(simulation)
    db_session.commit()
    db_session.refresh(simulation)
    
    response = client.get(f"/simulations/{simulation.id}/detailed")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == simulation.id
    assert data["name"] == "test_sim_detailed"
    assert "machine" in data
    assert data["machine"]["id"] == machine.id


def test_create_simulation_bare_sql(client: TestClient, db_session: Session):
    """Test creating simulation using bare SQL"""
    machine = db_session.query(Machine).first()
    
    response = client.post(
        f"/simulations/{999}/create-bare-sql",
        params={"name": "bare_sql_sim", "machine_id": machine.id}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert data["name"] == "bare_sql_sim"
    assert data["machine_id"] == machine.id
    assert data["status"] == "pending"


def test_simulation_not_found(client: TestClient):
    """Test getting non-existent simulation"""
    response = client.get("/simulations/99999")
    assert response.status_code == 404
