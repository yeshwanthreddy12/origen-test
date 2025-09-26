from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ConvergenceDataBase(BaseModel):
    simulation_id: int
    loss_value: float


class ConvergenceDataCreate(ConvergenceDataBase):
    pass


class ConvergenceDataResponse(ConvergenceDataBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


class ConvergenceData(ConvergenceDataBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


class ConvergenceGraphResponse(BaseModel):
    simulation_id: int
    data_points: List[ConvergenceDataResponse]
    is_complete: bool
