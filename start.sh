#!/bin/bash

echo "🚀 Starting Origen.ai Simulation Scheduling System..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Start the services
echo "📦 Starting services with Docker Compose..."
docker compose up --build -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if services are running
if curl -s http://localhost:8000/health > /dev/null; then
    echo "✅ Services are running!"
    echo ""
    echo "🌐 API Documentation: http://localhost:8000/docs"
    echo "📊 Alternative Docs: http://localhost:8000/redoc"
    echo "❤️  Health Check: http://localhost:8000/health"
    echo ""
    echo "🧪 To test the API, run: python test_api.py"
    echo "🛑 To stop services, run: docker compose down"
else
    echo "❌ Services failed to start. Check logs with: docker compose logs"
    exit 1
fi
