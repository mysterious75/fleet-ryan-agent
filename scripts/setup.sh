#!/bin/bash
# Fleet-Ryan Setup Script
# Automates initial setup and configuration

set -e

echo "🚛 Fleet-Ryan Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

# Check Docker Compose
if ! command -v docker compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo ""
    echo "⚠️  IMPORTANT: Edit .env file with your actual API keys:"
    echo "   - SAMSARA_API_TOKEN"
    echo "   - TELEGRAM_BOT_TOKEN"
    echo "   - FLEET_MANAGER_CHAT_ID"
    echo ""
    read -p "Press Enter to continue after editing .env..."
else
    echo "✅ .env file already exists"
fi

# Build and start services
echo ""
echo "🔨 Building Docker containers..."
docker compose build

echo ""
echo "🚀 Starting services..."
docker compose up -d

# Wait for services to be ready
echo ""
echo "⏳ Waiting for services to start..."
sleep 10

# Check service health
echo ""
echo "🏥 Checking service health..."

# Check PostgreSQL
if docker compose exec -T postgres pg_isready -U fleetryan > /dev/null 2>&1; then
    echo "✅ PostgreSQL is ready"
else
    echo "❌ PostgreSQL is not ready"
fi

# Check Redis
if docker compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis is ready"
else
    echo "❌ Redis is not ready"
fi

# Check Backend
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend API is ready"
else
    echo "⚠️  Backend API is starting (may take a moment)"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Fleet-Ryan setup complete!"
echo ""
echo "📊 Services:"
echo "   - Backend API: http://localhost:8000"
echo "   - API Docs: http://localhost:8000/docs"
echo "   - OpenClaw: http://localhost:18789"
echo ""
echo "🔧 Management:"
echo "   - View logs: docker compose logs -f"
echo "   - Stop services: docker compose down"
echo "   - Restart: docker compose restart"
echo ""
echo "📝 Next steps:"
echo "   1. Edit .env with your API keys"
echo "   2. Create Telegram bot via @BotFather"
echo "   3. Get Samsara API token from your account"
echo "   4. Test the API at http://localhost:8000/docs"
echo ""
