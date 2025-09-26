from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.database import get_db
from app.services.simulation_service import SimulationService
from app.schemas.simulation import (
    SimulationCreate, 
    SimulationResponse, 
    SimulationUpdate, 
    SimulationListResponse
)
from app.models.simulation import Simulation, SimulationStatus
from app.models.machine import Machine

router = APIRouter(prefix="/simulations", tags=["simulations"])


@router.post("/", response_model=SimulationResponse)
def create_simulation(simulation: SimulationCreate, db: Session = Depends(get_db)):
    """Create a new simulation"""
    service = SimulationService(db)
    
    # Check if machine exists
    machine = db.query(Machine).filter(Machine.id == simulation.machine_id).first()
    
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    return service.create_simulation(simulation)


@router.get("/", response_model=SimulationListResponse)
def list_simulations(
    status: Optional[SimulationStatus] = Query(None, description="Filter by simulation status"),
    order_by: str = Query("created_at", description="Order by field (name, created_at, updated_at)"),
    order_direction: str = Query("desc", description="Order direction (asc, desc)"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(100, ge=1, le=1000, description="Page size"),
    db: Session = Depends(get_db)
):
    """List all simulations with filtering and ordering"""
    service = SimulationService(db)
    
    skip = (page - 1) * size
    simulations = service.get_simulations(
        status=status,
        order_by=order_by,
        order_direction=order_direction,
        skip=skip,
        limit=size
    )
    
    # Get total count
    total_query = service.db.query(Simulation)
    if status:
        total_query = total_query.filter(Simulation.status == status)
    total = total_query.count()
    
    return SimulationListResponse(
        simulations=simulations,
        total=total,
        page=page,
        size=size
    )


@router.get("/{simulation_id}", response_model=SimulationResponse)
def get_simulation(simulation_id: int, db: Session = Depends(get_db)):
    """Get simulation details by ID"""
    service = SimulationService(db)
    simulation = service.get_simulation_with_machine_data(simulation_id)
    
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    return simulation


@router.get("/{simulation_id}/detailed", response_model=dict)
def get_simulation_detailed(simulation_id: int, db: Session = Depends(get_db)):
    """Get simulation with machine details using bare SQL"""
    service = SimulationService(db)
    simulation = service.get_simulation_with_machine(simulation_id)
    
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    return simulation


@router.put("/{simulation_id}", response_model=SimulationResponse)
def update_simulation(
    simulation_id: int, 
    simulation_update: SimulationUpdate, 
    db: Session = Depends(get_db)
):
    """Update simulation"""
    service = SimulationService(db)
    simulation = service.update_simulation(simulation_id, simulation_update)
    
    if not simulation:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    return simulation


@router.delete("/{simulation_id}")
def delete_simulation(simulation_id: int, db: Session = Depends(get_db)):
    """Delete simulation"""
    service = SimulationService(db)
    success = service.delete_simulation(simulation_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Simulation not found")
    
    return {"message": "Simulation deleted successfully"}


@router.post("/{simulation_id}/create-bare-sql", response_model=dict)
def create_simulation_bare_sql(
    simulation_id: int,
    name: str,
    machine_id: int,
    db: Session = Depends(get_db)
):
    """Create simulation using bare SQL (demonstration endpoint)"""
    service = SimulationService(db)
    
    # Check if machine exists
    machine = db.query(Machine).filter(Machine.id == machine_id).first()
    
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    return service.create_simulation_bare_sql(name, machine_id)
