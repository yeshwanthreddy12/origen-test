import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.models.simulation import Simulation
from app.models.machine import Machine
from app.models.convergence_data import ConvergenceData


def test_add_convergence_data(client: TestClient, db_session: Session):
    """Test adding convergence data"""
    # Create a simulation first
    machine = db_session.query(Machine).first()
    simulation = Simulation(name="test_conv_sim", machine_id=machine.id)
    db_session.add(simulation)
    db_session.commit()
    db_session.refresh(simulation)
    
    convergence_data = {
        "simulation_id": simulation.id,
        "loss_value": 0.5
    }
    
    response = client.post("/convergence/data", json=convergence_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["simulation_id"] == simulation.id
    assert data["loss_value"] == 0.5


def test_get_convergence_graph(client: TestClient, db_session: Session):
    """Test getting convergence graph data"""
    # Create a simulation and add some convergence data
    machine = db_session.query(Machine).first()
    simulation = Simulation(name="test_graph_sim", machine_id=machine.id)
    db_session.add(simulation)
    db_session.commit()
    db_session.refresh(simulation)
    
    # Add some convergence data
    for i in range(3):
        conv_data = ConvergenceData(
            simulation_id=simulation.id,
            loss_value=1.0 - (i * 0.2)
        )
        db_session.add(conv_data)
    db_session.commit()
    
    response = client.get(f"/convergence/{simulation.id}/graph")
    assert response.status_code == 200
    
    data = response.json()
    assert data["simulation_id"] == simulation.id
    assert "data_points" in data
    assert len(data["data_points"]) == 3


def test_get_convergence_data(client: TestClient, db_session: Session):
    """Test getting all convergence data for a simulation"""
    # Create a simulation and add some convergence data
    machine = db_session.query(Machine).first()
    simulation = Simulation(name="test_data_sim", machine_id=machine.id)
    db_session.add(simulation)
    db_session.commit()
    db_session.refresh(simulation)
    
    # Add some convergence data
    conv_data = ConvergenceData(
        simulation_id=simulation.id,
        loss_value=0.8
    )
    db_session.add(conv_data)
    db_session.commit()
    
    response = client.get(f"/convergence/{simulation.id}/data")
    assert response.status_code == 200
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["loss_value"] == 0.8


def test_add_convergence_data_bare_sql(client: TestClient, db_session: Session):
    """Test adding convergence data using bare SQL"""
    # Create a simulation first
    machine = db_session.query(Machine).first()
    simulation = Simulation(name="test_bare_sql_sim", machine_id=machine.id)
    db_session.add(simulation)
    db_session.commit()
    db_session.refresh(simulation)
    
    response = client.post(
        f"/convergence/{simulation.id}/add-bare-sql",
        params={"loss_value": 0.3}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert data["simulation_id"] == simulation.id
    assert data["loss_value"] == 0.3


def test_convergence_simulation_not_found(client: TestClient):
    """Test convergence endpoints with non-existent simulation"""
    response = client.get("/convergence/99999/graph")
    assert response.status_code == 404
