from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from app.db.database import Base


class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    cpu = Column(String, nullable=False)
    gpu = Column(String, nullable=False)
    memory = Column(Float, nullable=False)  # in GB
    status = Column(String, default="available")  # available, busy, maintenance

    # Relationship
    simulations = relationship("Simulation", back_populates="machine")
