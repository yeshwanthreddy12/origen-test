from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.machine import Machine
from app.schemas.machine import MachineCreate


class MachineService:
    def __init__(self, db: Session):
        self.db = db

    def get_machines(self) -> List[Machine]:
        """Get all machines using ORM"""
        return self.db.query(Machine).all()

    def get_machine(self, machine_id: int) -> Optional[Machine]:
        """Get machine by ID using ORM"""
        return self.db.query(Machine).filter(Machine.id == machine_id).first()

    def create_machine(self, machine: MachineCreate) -> Machine:
        """Create a new machine using ORM"""
        db_machine = Machine(**machine.dict())
        self.db.add(db_machine)
        self.db.commit()
        self.db.refresh(db_machine)
        return db_machine

    def update_machine_status(self, machine_id: int, status: str) -> Optional[Machine]:
        """Update machine status using ORM"""
        db_machine = self.get_machine(machine_id)
        if not db_machine:
            return None
        
        db_machine.status = status
        self.db.commit()
        self.db.refresh(db_machine)
        return db_machine
