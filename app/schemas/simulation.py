from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.simulation import SimulationStatus


class SimulationBase(BaseModel):
    name: str
    machine_id: int


class SimulationCreate(SimulationBase):
    pass


class SimulationUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[SimulationStatus] = None
    machine_id: Optional[int] = None


class SimulationResponse(SimulationBase):
    id: int
    status: SimulationStatus
    created_at: datetime
    updated_at: datetime
    machine: Optional[dict] = None

    class Config:
        from_attributes = True


class Simulation(SimulationBase):
    id: int
    status: SimulationStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class SimulationListResponse(BaseModel):
    simulations: List[SimulationResponse]
    total: int
    page: int
    size: int
