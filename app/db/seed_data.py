"""
Seed/fixture data for machines
"""
from sqlalchemy.orm import Session
from app.models.machine import Machine


def seed_machines(db: Session):
    """Add seed data for machines if they don't exist"""
    machines_data = [
        {
            "name": "gpu-cluster-01",
            "cpu": "Intel Xeon E5-2686 v4",
            "gpu": "NVIDIA Tesla V100",
            "memory": 32.0,
            "status": "available"
        },
        {
            "name": "gpu-cluster-02", 
            "cpu": "Intel Xeon E5-2686 v4",
            "gpu": "NVIDIA Tesla V100",
            "memory": 32.0,
            "status": "available"
        },
        {
            "name": "cpu-cluster-01",
            "cpu": "Intel Xeon Gold 6248R",
            "gpu": "None",
            "memory": 128.0,
            "status": "available"
        },
        {
            "name": "gpu-cluster-03",
            "cpu": "AMD EPYC 7742",
            "gpu": "NVIDIA A100",
            "memory": 64.0,
            "status": "maintenance"
        },
        {
            "name": "hybrid-cluster-01",
            "cpu": "Intel Xeon Platinum 8280",
            "gpu": "NVIDIA RTX 3090",
            "memory": 256.0,
            "status": "available"
        }
    ]
    
    for machine_data in machines_data:
        existing_machine = db.query(Machine).filter(Machine.name == machine_data["name"]).first()
        if not existing_machine:
            machine = Machine(**machine_data)
            db.add(machine)
    
    db.commit()
