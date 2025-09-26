from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from app.models.simulation import Simulation, SimulationStatus
from app.schemas.simulation import SimulationCreate, SimulationUpdate
from app.models.machine import Machine


class SimulationService:
    def __init__(self, db: Session):
        self.db = db

    def create_simulation(self, simulation: SimulationCreate) -> dict:
        """Create a new simulation using ORM"""
        db_simulation = Simulation(**simulation.dict())
        self.db.add(db_simulation)
        self.db.commit()
        self.db.refresh(db_simulation)
        
        # Return as dict with machine data
        return {
            "id": db_simulation.id,
            "name": db_simulation.name,
            "status": db_simulation.status,
            "machine_id": db_simulation.machine_id,
            "created_at": db_simulation.created_at,
            "updated_at": db_simulation.updated_at,
            "machine": {
                "id": db_simulation.machine.id,
                "name": db_simulation.machine.name,
                "cpu": db_simulation.machine.cpu,
                "gpu": db_simulation.machine.gpu,
                "memory": db_simulation.machine.memory,
                "status": db_simulation.machine.status
            } if db_simulation.machine else None
        }

    def get_simulation(self, simulation_id: int) -> Optional[Simulation]:
        """Get simulation by ID using ORM"""
        return self.db.query(Simulation).filter(Simulation.id == simulation_id).first()
    
    def get_simulation_with_machine_data(self, simulation_id: int) -> Optional[dict]:
        """Get simulation with machine data serialized as dict"""
        simulation = self.db.query(Simulation).filter(Simulation.id == simulation_id).first()
        if not simulation:
            return None
        
        result = {
            "id": simulation.id,
            "name": simulation.name,
            "status": simulation.status,
            "machine_id": simulation.machine_id,
            "created_at": simulation.created_at,
            "updated_at": simulation.updated_at,
            "machine": {
                "id": simulation.machine.id,
                "name": simulation.machine.name,
                "cpu": simulation.machine.cpu,
                "gpu": simulation.machine.gpu,
                "memory": simulation.machine.memory,
                "status": simulation.machine.status
            } if simulation.machine else None
        }
        return result

    def get_simulations(
        self, 
        status: Optional[SimulationStatus] = None,
        order_by: str = "created_at",
        order_direction: str = "desc",
        skip: int = 0,
        limit: int = 100
    ) -> List[dict]:
        """Get simulations with filtering and ordering using ORM"""
        query = self.db.query(Simulation)
        
        if status:
            query = query.filter(Simulation.status == status)
        
        # Order by
        if order_by == "name":
            order_column = Simulation.name
        elif order_by == "created_at":
            order_column = Simulation.created_at
        elif order_by == "updated_at":
            order_column = Simulation.updated_at
        else:
            order_column = Simulation.created_at
        
        if order_direction == "desc":
            query = query.order_by(order_column.desc())
        else:
            query = query.order_by(order_column.asc())
        
        simulations = query.offset(skip).limit(limit).all()
        
        # Convert to dict format with machine data
        result = []
        for sim in simulations:
            result.append({
                "id": sim.id,
                "name": sim.name,
                "status": sim.status,
                "machine_id": sim.machine_id,
                "created_at": sim.created_at,
                "updated_at": sim.updated_at,
                "machine": {
                    "id": sim.machine.id,
                    "name": sim.machine.name,
                    "cpu": sim.machine.cpu,
                    "gpu": sim.machine.gpu,
                    "memory": sim.machine.memory,
                    "status": sim.machine.status
                } if sim.machine else None
            })
        
        return result

    def update_simulation(self, simulation_id: int, simulation_update: SimulationUpdate) -> Optional[Simulation]:
        """Update simulation using ORM"""
        db_simulation = self.get_simulation(simulation_id)
        if not db_simulation:
            return None
        
        update_data = simulation_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_simulation, field, value)
        
        self.db.commit()
        self.db.refresh(db_simulation)
        return db_simulation

    def delete_simulation(self, simulation_id: int) -> bool:
        """Delete simulation using ORM"""
        db_simulation = self.get_simulation(simulation_id)
        if not db_simulation:
            return False
        
        self.db.delete(db_simulation)
        self.db.commit()
        return True

    def get_simulation_with_machine(self, simulation_id: int) -> Optional[dict]:
        """Get simulation with machine details using BARE SQL (READ operation)"""
        query = text("""
            SELECT 
                s.id,
                s.name,
                s.status,
                s.machine_id,
                s.created_at,
                s.updated_at,
                m.name as machine_name,
                m.cpu,
                m.gpu,
                m.memory,
                m.status as machine_status
            FROM simulations s
            JOIN machines m ON s.machine_id = m.id
            WHERE s.id = :simulation_id
        """)
        
        result = self.db.execute(query, {"simulation_id": simulation_id}).fetchone()
        if not result:
            return None
        
        return {
            "id": result.id,
            "name": result.name,
            "status": result.status,
            "machine_id": result.machine_id,
            "created_at": result.created_at,
            "updated_at": result.updated_at,
            "machine": {
                "id": result.machine_id,
                "name": result.machine_name,
                "cpu": result.cpu,
                "gpu": result.gpu,
                "memory": result.memory,
                "status": result.machine_status
            }
        }

    def create_simulation_bare_sql(self, name: str, machine_id: int) -> dict:
        """Create simulation using BARE SQL (WRITE operation)"""
        query = text("""
            INSERT INTO simulations (name, status, machine_id, created_at, updated_at)
            VALUES (:name, 'pending', :machine_id, NOW(), NOW())
            RETURNING id, name, status, machine_id, created_at, updated_at
        """)
        
        result = self.db.execute(query, {"name": name, "machine_id": machine_id}).fetchone()
        self.db.commit()
        
        return {
            "id": result.id,
            "name": result.name,
            "status": result.status,
            "machine_id": result.machine_id,
            "created_at": result.created_at,
            "updated_at": result.updated_at
        }
