from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MachineBase(BaseModel):
    name: str
    cpu: str
    gpu: str
    memory: float
    status: str = "available"


class MachineCreate(MachineBase):
    pass


class MachineResponse(MachineBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Machine(MachineBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True
