# Origen.ai Simulation Scheduling System

A FastAPI-based backend service for managing simulations, machines, and convergence data with real-time monitoring capabilities.

## What This Application Does

This is a simulation management system that allows you to:
- Create and manage simulation jobs
- Track available computing machines
- Monitor simulation convergence data in real-time
- Stream live updates via WebSocket connections

## Prerequisites

Before you start, make sure you have:
- **Docker** and **Docker Compose** installed on your system
- **Python 3.11+** (only needed for local development)

## Quick Start with Docker (Recommended)

### Step 1: Start the Application

Open your terminal and navigate to the project directory:

```bash
cd "origen new"
```

Start all services (database + application):

```bash
docker-compose up --build
```

This will:
- Download PostgreSQL database image
- Build the Python application
- Start both services
- Create database tables automatically
- Seed initial machine data

### Step 2: Verify It's Working

Once the containers are running, open your browser and check:

1. **API Documentation**: http://localhost:8000/docs
2. **Health Check**: http://localhost:8000/health
3. **Root Endpoint**: http://localhost:8000/

You should see:
- The Swagger UI documentation page
- A health check response: `{"status": "healthy"}`
- A welcome message at the root endpoint

### Step 3: Test the API

You can test the API using the interactive documentation at http://localhost:8000/docs, or use curl:

```bash
# Check if the API is responding
curl http://localhost:8000/health

# List all machines
curl http://localhost:8000/machines/

# List all simulations
curl http://localhost:8000/simulations/
```

## Running Without Docker (Local Development)

If you prefer to run the application locally without Docker:

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set Up PostgreSQL Database

You need a PostgreSQL database running locally. You can:

**Option A: Use Docker for just the database**
```bash
docker run --name postgres-db -e POSTGRES_DB=origen_simulations -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres:15
```

**Option B: Install PostgreSQL locally**
- Install PostgreSQL on your system
- Create a database named `origen_simulations`
- Make sure it's running on port 5432

### Step 3: Set Environment Variable

```bash
export DATABASE_URL="postgresql://postgres:password@localhost:5432/origen_simulations"
```

### Step 4: Run the Application

```bash
uvicorn app.main:app --reload
```

The application will start on http://localhost:8000

## How to Check If It's Working

### 1. Basic Health Check

First, make sure the application is running:

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

### 2. Check API Documentation

Open your browser and go to: http://localhost:8000/docs

You should see the Swagger UI with all available endpoints.

### 3. Test Core Functionality

**Test Machine Management:**
```bash
# List all machines
curl http://localhost:8000/machines/

# Create a new machine
curl -X POST http://localhost:8000/machines/ \
  -H "Content-Type: application/json" \
  -d '{"name": "test-machine", "cpu": "Intel i7", "gpu": "RTX 3080", "memory": 32, "status": "available"}'
```

**Test Simulation Management:**
```bash
# List all simulations
curl http://localhost:8000/simulations/

# Create a new simulation
curl -X POST http://localhost:8000/simulations/ \
  -H "Content-Type: application/json" \
  -d '{"name": "test-simulation", "machine_id": 1}'
```

**Test Convergence Data:**
```bash
# Add convergence data
curl -X POST http://localhost:8000/convergence/data \
  -H "Content-Type: application/json" \
  -d '{"simulation_id": 1, "loss_value": 0.5}'

# Get convergence graph data
curl http://localhost:8000/convergence/1/graph
```

### 4. Test WebSocket Connection

You can test the WebSocket connection using a simple HTML file or a WebSocket client:

```html
<!DOCTYPE html>
<html>
<head>
    <title>WebSocket Test</title>
</head>
<body>
    <div id="messages"></div>
    <script>
        const ws = new WebSocket('ws://localhost:8000/ws/convergence/1');
        const messages = document.getElementById('messages');
        
        ws.onopen = function(event) {
            messages.innerHTML += '<p>Connected to WebSocket</p>';
        };
        
        ws.onmessage = function(event) {
            messages.innerHTML += '<p>Received: ' + event.data + '</p>';
        };
        
        ws.onerror = function(error) {
            messages.innerHTML += '<p>Error: ' + error + '</p>';
        };
    </script>
</body>
</html>
```

## Troubleshooting

### Common Issues

**1. Port Already in Use**
```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process if needed
kill -9 <PID>
```

**2. Database Connection Issues**
```bash
# Check if PostgreSQL container is running
docker ps

# Check database logs
docker-compose logs db
```

**3. Application Won't Start**
```bash
# Check application logs
docker-compose logs app

# Rebuild containers
docker-compose down
docker-compose up --build
```

**4. Permission Issues (Linux/Mac)**
```bash
# Fix file permissions
sudo chown -R $USER:$USER .
```

### Docker Commands Reference

```bash
# Start services
docker-compose up

# Start in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs

# View logs for specific service
docker-compose logs app
docker-compose logs db

# Rebuild and start
docker-compose up --build

# Remove everything (including volumes)
docker-compose down -v
```

## Running Tests

To make sure everything is working correctly, run the test suite:

```bash
# Using Docker
docker-compose exec app pytest

# Or run tests locally (if you have Python installed)
pytest
```

## Project Structure

```
app/
├── main.py                 # FastAPI application entry point
├── models/                 # Database models
├── schemas/                # Request/response schemas
├── routes/                 # API endpoints
├── services/               # Business logic
└── db/                     # Database configuration
```

## API Endpoints Overview

- **Health Check**: `GET /health`
- **Machines**: `GET /machines/`, `POST /machines/`
- **Simulations**: `GET /simulations/`, `POST /simulations/`
- **Convergence Data**: `POST /convergence/data`, `GET /convergence/{id}/graph`
- **WebSocket**: `WS /ws/convergence/{simulation_id}`

For detailed API documentation, visit: http://localhost:8000/docs

## Production Deployment

For production deployment, consider:

1. **Environment Variables**: Set proper database credentials
2. **CORS Settings**: Configure allowed origins
3. **SSL/HTTPS**: Use proper certificates
4. **Database Security**: Use strong passwords and network security
5. **Monitoring**: Add logging and health monitoring
6. **Scaling**: Use load balancers for multiple instances

## Need Help?

If you encounter issues:

1. Check the logs: `docker-compose logs`
2. Verify all services are running: `docker ps`
3. Test the health endpoint: `curl http://localhost:8000/health`
4. Check the API documentation: http://localhost:8000/docs


