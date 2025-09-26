from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base


class ConvergenceData(Base):
    __tablename__ = "convergence_data"

    id = Column(Integer, primary_key=True, index=True)
    simulation_id = Column(Integer, ForeignKey("simulations.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    loss_value = Column(Float, nullable=False)

    # Relationship
    simulation = relationship("Simulation", back_populates="convergence_data")
