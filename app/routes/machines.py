from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.services.machine_service import MachineService
from app.schemas.machine import MachineCreate, MachineResponse

router = APIRouter(prefix="/machines", tags=["machines"])


@router.get("/", response_model=List[MachineResponse])
def list_machines(db: Session = Depends(get_db)):
    """List all available machines"""
    service = MachineService(db)
    return service.get_machines()


@router.get("/{machine_id}", response_model=MachineResponse)
def get_machine(machine_id: int, db: Session = Depends(get_db)):
    """Get machine details by ID"""
    service = MachineService(db)
    machine = service.get_machine(machine_id)
    
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    return machine


@router.post("/", response_model=MachineResponse)
def create_machine(machine: MachineCreate, db: Session = Depends(get_db)):
    """Create a new machine"""
    service = MachineService(db)
    return service.create_machine(machine)


@router.patch("/{machine_id}/status")
def update_machine_status(
    machine_id: int, 
    status: str, 
    db: Session = Depends(get_db)
):
    """Update machine status"""
    service = MachineService(db)
    machine = service.update_machine_status(machine_id, status)
    
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    return {"message": f"Machine {machine_id} status updated to {status}"}
