#!/bin/bash

echo "🎧 Starting DJ Setlist AI..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running. Please start Docker first."
    exit 1
fi

# Build and start containers
echo "📦 Building containers..."
docker-compose build

echo ""
echo "🚀 Starting services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check container status
echo ""
echo "📊 Container Status:"
docker-compose ps

echo ""
echo "✅ DJ Setlist AI is running!"
echo ""
echo "🌐 Frontend:    http://localhost:3000"
echo "🔌 Backend API: http://localhost:8000"
echo "📚 API Docs:    http://localhost:8000/docs"
echo "🗄️  pgAdmin:     http://localhost:5050 (admin@example.com / admin)"
echo ""
echo "To stop: docker-compose down"
echo "To view logs: docker-compose logs -f"
