from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List, Optional
import json
from app.db.database import get_db
from app.services.convergence_service import ConvergenceService
from app.schemas.convergence_data import (
    ConvergenceDataCreate, 
    ConvergenceDataResponse,
    ConvergenceGraphResponse
)

router = APIRouter(prefix="/convergence", tags=["convergence"])


@router.post("/data", response_model=ConvergenceDataResponse)
def add_convergence_data(
    convergence_data: ConvergenceDataCreate, 
    db: Session = Depends(get_db)
):
    """Add convergence data point"""
    service = ConvergenceService(db)
    return service.add_convergence_data(convergence_data)


@router.get("/{simulation_id}/graph", response_model=ConvergenceGraphResponse)
def get_convergence_graph(simulation_id: int, db: Session = Depends(get_db)):
    """Get convergence graph data for a simulation"""
    service = ConvergenceService(db)
    
    # Check if simulation exists
    from app.models.simulation import Simulation
    simulation = db.query(Simulation).filter(Simulation.id == simulation_id).first()
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    graph_data = service.get_convergence_graph_data(simulation_id)
    return ConvergenceGraphResponse(**graph_data)


@router.get("/{simulation_id}/stream")
def stream_convergence_data(
    simulation_id: int,
    last_timestamp: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Stream convergence data for real-time updates"""
    service = ConvergenceService(db)
    
    # Check if simulation exists
    from app.models.simulation import Simulation
    simulation = db.query(Simulation).filter(Simulation.id == simulation_id).first()
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    data_points = service.get_convergence_data_streaming(simulation_id, last_timestamp)
    is_finished = service.is_simulation_finished(simulation_id)
    
    return {
        "simulation_id": simulation_id,
        "data_points": data_points,
        "is_complete": is_finished
    }


@router.get("/{simulation_id}/data", response_model=List[ConvergenceDataResponse])
def get_convergence_data(simulation_id: int, db: Session = Depends(get_db)):
    """Get all convergence data for a simulation"""
    service = ConvergenceService(db)
    
    # Check if simulation exists
    from app.models.simulation import Simulation
    simulation = db.query(Simulation).filter(Simulation.id == simulation_id).first()
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    return service.get_convergence_data(simulation_id)


@router.post("/{simulation_id}/add-bare-sql", response_model=dict)
def add_convergence_data_bare_sql(
    simulation_id: int,
    loss_value: float,
    db: Session = Depends(get_db)
):
    """Add convergence data using bare SQL (demonstration endpoint)"""
    service = ConvergenceService(db)
    
    # Check if simulation exists
    from app.models.simulation import Simulation
    simulation = db.query(Simulation).filter(Simulation.id == simulation_id).first()
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    return service.add_convergence_data_bare_sql(simulation_id, loss_value)
