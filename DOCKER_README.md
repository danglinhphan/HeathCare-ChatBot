# Healthcare Chatbot - Docker Setup

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose installed
- At least 4GB RAM available
- Ports 3000 and 8000 available

### Production Build
```bash
# Build and start all services
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Development Build
```bash
# Start development environment with hot reload
docker-compose -f docker-compose.dev.yml up --build -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop services
docker-compose -f docker-compose.dev.yml down
```

### Using Scripts
```bash
# Windows
start.bat

# Linux/Mac
chmod +x start.sh
./start.sh
```

## 📋 Services

| Service | Port | URL | Description |
|---------|------|-----|-------------|
| Frontend | 3000 | http://localhost:3000 | Next.js React App |
| Backend | 8000 | http://localhost:8000 | FastAPI Backend |
| API Docs | 8000 | http://localhost:8000/docs | Swagger UI |

## 🔧 Useful Commands

```bash
# Rebuild specific service
docker-compose build frontend
docker-compose build backend

# View service logs
docker-compose logs frontend
docker-compose logs backend

# Execute commands in running container
docker-compose exec frontend sh
docker-compose exec backend bash

# Remove all containers and volumes
docker-compose down -v

# Remove images
docker-compose down --rmi all
```

## 🐛 Troubleshooting

### Port Conflicts
If ports 3000 or 8000 are in use:
```bash
# Check what's using the ports
netstat -an | grep 3000
netstat -an | grep 8000

# Kill processes if needed (Windows)
taskkill /F /PID <PID>
```

### Container Issues
```bash
# Restart specific service
docker-compose restart frontend
docker-compose restart backend

# Rebuild without cache
docker-compose build --no-cache

# View container status
docker-compose ps
```

### Clean Up
```bash
# Remove all stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Nuclear option - clean everything
docker system prune -a
```

## 📝 Environment Variables

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### Backend (.env)
```
ENVIRONMENT=production
DATABASE_URL=your_database_url
GEMINI_API_KEY=your_gemini_key
```
