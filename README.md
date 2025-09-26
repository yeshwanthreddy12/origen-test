# Origen.ai Simulation Scheduling System

A Python-based backend service for managing simulations, machines, and convergence data with real-time monitoring capabilities.

## 🚀 Features

- **Simulation Management**: Create, list, update, and delete simulations
- **Machine Management**: Manage available computing resources
- **Convergence Monitoring**: Real-time convergence graph data streaming
- **WebSocket Support**: Live updates for convergence data
- **Database Operations**: Mix of ORM and bare SQL operations
- **Comprehensive Testing**: Unit tests with pytest
- **Auto-generated API Docs**: FastAPI OpenAPI documentation

## 🛠 Tech Stack

- **Framework**: FastAPI (async support)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Validation**: Pydantic
- **Testing**: pytest
- **Containerization**: Docker + Docker Compose
- **Real-time**: WebSockets

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.11+ (for local development)

## 🚀 Quick Start

### Using Docker (Recommended)

1. **Clone and navigate to the project**:
   ```bash
   cd "origen new"
   ```

2. **Start the services**:
   ```bash
   docker-compose up --build
   ```

3. **Access the API**:
   - API Documentation: http://localhost:8000/docs
   - Alternative Docs: http://localhost:8000/redoc
   - Health Check: http://localhost:8000/health

### Local Development

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL database**:
   ```bash
   # Start PostgreSQL (adjust connection details as needed)
   createdb origen_simulations
   ```

3. **Set environment variable**:
   ```bash
   export DATABASE_URL="postgresql://postgres:password@localhost:5432/origen_simulations"
   ```

4. **Run the application**:
   ```bash
   uvicorn app.main:app --reload
   ```

## 🏗 Architecture

### Project Structure

```
app/
├── main.py                 # FastAPI application entry point
├── models/                 # SQLAlchemy database models
│   ├── machine.py
│   ├── simulation.py
│   └── convergence_data.py
├── schemas/                # Pydantic request/response schemas
│   ├── machine.py
│   ├── simulation.py
│   └── convergence_data.py
├── routes/                 # API route handlers
│   ├── simulations.py
│   ├── machines.py
│   ├── convergence.py
│   └── websocket.py
├── services/               # Business logic layer
│   ├── simulation_service.py
│   ├── machine_service.py
│   └── convergence_service.py
└── db/                     # Database configuration
    ├── database.py
    └── seed_data.py
```

### Database Schema

#### Machines Table
- `id` (PK): Primary key
- `name`: Machine identifier
- `cpu`: CPU specification
- `gpu`: GPU specification
- `memory`: Memory in GB
- `status`: Current status (available, busy, maintenance)

#### Simulations Table
- `id` (PK): Primary key
- `name`: Simulation name
- `status`: Simulation status (pending, running, finished)
- `machine_id` (FK): Reference to machines table
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

#### Convergence Data Table
- `id` (PK): Primary key
- `simulation_id` (FK): Reference to simulations table
- `timestamp`: Data point timestamp
- `loss_value`: Loss value at this point

## 🔌 API Endpoints

### Simulations

- `GET /simulations/` - List simulations with filtering and ordering
- `POST /simulations/` - Create new simulation
- `GET /simulations/{id}` - Get simulation details
- `GET /simulations/{id}/detailed` - Get simulation with machine details (bare SQL)
- `PUT /simulations/{id}` - Update simulation
- `DELETE /simulations/{id}` - Delete simulation
- `POST /simulations/{id}/create-bare-sql` - Create simulation using bare SQL

### Machines

- `GET /machines/` - List all machines
- `GET /machines/{id}` - Get machine details
- `POST /machines/` - Create new machine
- `PATCH /machines/{id}/status` - Update machine status

### Convergence Data

- `POST /convergence/data` - Add convergence data point
- `GET /convergence/{simulation_id}/graph` - Get convergence graph data
- `GET /convergence/{simulation_id}/stream` - Stream convergence data
- `GET /convergence/{simulation_id}/data` - Get all convergence data
- `POST /convergence/{simulation_id}/add-bare-sql` - Add data using bare SQL

### WebSocket

- `WS /ws/convergence/{simulation_id}` - Real-time convergence updates

## 🔧 Bare SQL Operations

The system includes both ORM and bare SQL operations as requested:

### Write Operations (Bare SQL)
- **Simulation Creation**: `create_simulation_bare_sql()` in `SimulationService`
- **Convergence Data Addition**: `add_convergence_data_bare_sql()` in `ConvergenceService`

### Read Operations (Bare SQL)
- **Simulation with Machine Details**: `get_simulation_with_machine()` in `SimulationService`
- **Convergence Graph Data**: `get_convergence_graph_data()` in `ConvergenceService`

These operations are clearly marked in the code with comments and are accessible via dedicated API endpoints.

## 🧪 Testing

Run the test suite:

```bash
# Using Docker
docker-compose exec app pytest

# Local development
pytest
```

### Test Coverage

- Unit tests for all API endpoints
- Database operation testing
- WebSocket functionality testing
- Error handling validation

## 📊 Database Migrations

The project uses Alembic for database migrations:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

## 🔄 Real-time Features

### WebSocket Integration

The system provides real-time convergence data updates via WebSocket:

```javascript
// Example WebSocket client
const ws = new WebSocket('ws://localhost:8000/ws/convergence/1');

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('New convergence data:', data);
};
```

### Streaming Endpoints

- **Convergence Stream**: Get incremental updates since last timestamp
- **WebSocket**: Real-time bidirectional communication
- **Graph Data**: Complete convergence graph with completion status

## 🐳 Docker Configuration

### Services

- **app**: FastAPI application (port 8000)
- **db**: PostgreSQL database (port 5432)

### Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `POSTGRES_DB`: Database name
- `POSTGRES_USER`: Database user
- `POSTGRES_PASSWORD`: Database password

## 📈 Performance Considerations

- **Async Support**: FastAPI provides async request handling
- **Connection Pooling**: SQLAlchemy connection management
- **Efficient Queries**: Optimized database queries with proper indexing
- **Real-time Updates**: WebSocket for live data streaming

## 🔒 Security Notes

- CORS is configured for development (configure appropriately for production)
- Input validation via Pydantic schemas
- SQL injection protection through parameterized queries
- Database connection security through environment variables

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**: Set production database URL
2. **CORS Configuration**: Update allowed origins
3. **Database Security**: Use strong passwords and SSL
4. **Monitoring**: Add logging and monitoring
5. **Scaling**: Consider horizontal scaling for high load

### Health Checks

- `GET /health` - Application health status
- Database connectivity validation
- Service dependency checks

## 📝 API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request


