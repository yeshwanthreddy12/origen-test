from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
from app.models.convergence_data import ConvergenceData
from app.schemas.convergence_data import ConvergenceDataCreate
from app.models.simulation import Simulation, SimulationStatus


class ConvergenceService:
    def __init__(self, db: Session):
        self.db = db

    def add_convergence_data(self, convergence_data: ConvergenceDataCreate) -> ConvergenceData:
        """Add convergence data point using ORM"""
        db_data = ConvergenceData(**convergence_data.dict())
        self.db.add(db_data)
        self.db.commit()
        self.db.refresh(db_data)
        return db_data

    def get_convergence_data(self, simulation_id: int) -> List[ConvergenceData]:
        """Get all convergence data for a simulation using ORM"""
        return self.db.query(ConvergenceData).filter(
            ConvergenceData.simulation_id == simulation_id
        ).order_by(ConvergenceData.timestamp).all()

    def get_convergence_data_streaming(self, simulation_id: int, last_timestamp: Optional[str] = None) -> List[ConvergenceData]:
        """Get convergence data for streaming (new data since last_timestamp) using ORM"""
        query = self.db.query(ConvergenceData).filter(
            ConvergenceData.simulation_id == simulation_id
        )
        
        if last_timestamp:
            query = query.filter(ConvergenceData.timestamp > last_timestamp)
        
        return query.order_by(ConvergenceData.timestamp).all()

    def is_simulation_finished(self, simulation_id: int) -> bool:
        """Check if simulation is finished using ORM"""
        simulation = self.db.query(Simulation).filter(Simulation.id == simulation_id).first()
        return simulation.status == SimulationStatus.FINISHED if simulation else False

    def get_convergence_graph_data(self, simulation_id: int) -> dict:
        """Get convergence graph data using BARE SQL (READ operation)"""
        query = text("""
            SELECT 
                cd.id,
                cd.simulation_id,
                cd.timestamp,
                cd.loss_value,
                s.status as simulation_status
            FROM convergence_data cd
            JOIN simulations s ON cd.simulation_id = s.id
            WHERE cd.simulation_id = :simulation_id
            ORDER BY cd.timestamp ASC
        """)
        
        result = self.db.execute(query, {"simulation_id": simulation_id}).fetchall()
        
        data_points = []
        for row in result:
            data_points.append({
                "id": row.id,
                "simulation_id": row.simulation_id,
                "timestamp": row.timestamp,
                "loss_value": row.loss_value
            })
        
        is_finished = any(row.simulation_status == "finished" for row in result) if result else False
        
        return {
            "simulation_id": simulation_id,
            "data_points": data_points,
            "is_complete": is_finished
        }

    def add_convergence_data_bare_sql(self, simulation_id: int, loss_value: float) -> dict:
        """Add convergence data using BARE SQL (WRITE operation)"""
        query = text("""
            INSERT INTO convergence_data (simulation_id, loss_value, timestamp)
            VALUES (:simulation_id, :loss_value, NOW())
            RETURNING id, simulation_id, loss_value, timestamp
        """)
        
        result = self.db.execute(query, {
            "simulation_id": simulation_id,
            "loss_value": loss_value
        }).fetchone()
        self.db.commit()
        
        return {
            "id": result.id,
            "simulation_id": result.simulation_id,
            "loss_value": result.loss_value,
            "timestamp": result.timestamp
        }
