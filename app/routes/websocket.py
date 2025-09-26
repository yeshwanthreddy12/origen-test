from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.services.convergence_service import ConvergenceService
from app.models.simulation import Simulation
import json
import asyncio
from typing import Dict, List

router = APIRouter(prefix="/ws", tags=["websocket"])

# Store active connections
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, simulation_id: int):
        await websocket.accept()
        if simulation_id not in self.active_connections:
            self.active_connections[simulation_id] = []
        self.active_connections[simulation_id].append(websocket)

    def disconnect(self, websocket: WebSocket, simulation_id: int):
        if simulation_id in self.active_connections:
            self.active_connections[simulation_id].remove(websocket)
            if not self.active_connections[simulation_id]:
                del self.active_connections[simulation_id]

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_to_simulation(self, message: str, simulation_id: int):
        if simulation_id in self.active_connections:
            for connection in self.active_connections[simulation_id]:
                try:
                    await connection.send_text(message)
                except:
                    # Remove broken connections
                    self.active_connections[simulation_id].remove(connection)

manager = ConnectionManager()


@router.websocket("/convergence/{simulation_id}")
async def websocket_convergence_endpoint(websocket: WebSocket, simulation_id: int):
    """WebSocket endpoint for real-time convergence graph updates"""
    await manager.connect(websocket, simulation_id)
    
    try:
        # Check if simulation exists
        db = next(get_db())
        simulation = db.query(Simulation).filter(Simulation.id == simulation_id).first()
        if not simulation:
            await websocket.send_text(json.dumps({"error": "Simulation not found"}))
            await websocket.close()
            return
        
        # Send initial data
        service = ConvergenceService(db)
        initial_data = service.get_convergence_data(simulation_id)
        
        await websocket.send_text(json.dumps({
            "type": "initial_data",
            "simulation_id": simulation_id,
            "data_points": [
                {
                    "id": data.id,
                    "timestamp": data.timestamp.isoformat(),
                    "loss_value": data.loss_value
                } for data in initial_data
            ]
        }))
        
        # Keep connection alive and send periodic updates
        last_timestamp = None
        while True:
            try:
                # Check for new data every 2 seconds
                await asyncio.sleep(2)
                
                new_data = service.get_convergence_data_streaming(simulation_id, last_timestamp)
                is_finished = service.is_simulation_finished(simulation_id)
                
                if new_data:
                    last_timestamp = new_data[-1].timestamp.isoformat()
                    
                    await manager.broadcast_to_simulation(json.dumps({
                        "type": "new_data",
                        "simulation_id": simulation_id,
                        "data_points": [
                            {
                                "id": data.id,
                                "timestamp": data.timestamp.isoformat(),
                                "loss_value": data.loss_value
                            } for data in new_data
                        ],
                        "is_complete": is_finished
                    }), simulation_id)
                
                if is_finished:
                    await manager.broadcast_to_simulation(json.dumps({
                        "type": "simulation_finished",
                        "simulation_id": simulation_id
                    }), simulation_id)
                    break
                    
            except Exception as e:
                print(f"Error in WebSocket loop: {e}")
                break
                
    except WebSocketDisconnect:
        manager.disconnect(websocket, simulation_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket, simulation_id)
    finally:
        db.close()
