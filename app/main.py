from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import simulations_router, machines_router, convergence_router, websocket_router
from app.db.database import engine, Base
from app.db.seed_data import seed_machines
from sqlalchemy.orm import Session

# Create database tables
Base.metadata.create_all(bind=engine)

# Seed initial data
db = Session(engine)
try:
    seed_machines(db)
finally:
    db.close()

app = FastAPI(
    title="Origen.ai Simulation Scheduling System",
    description="Backend service for managing simulations, machines, and convergence data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(simulations_router)
app.include_router(machines_router)
app.include_router(convergence_router)
app.include_router(websocket_router)


@app.get("/")
def read_root():
    return {
        "message": "Origen.ai Simulation Scheduling System API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
