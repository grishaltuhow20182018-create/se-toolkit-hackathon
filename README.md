# 🎧 DJ Setlist AI

**AI-powered DJ setlist generator with seamless track matching and playlist management**

---

## 📸 Demo

![DJ Setlist AI Interface](https://via.placeholder.com/800x450/1a1a2e/16213e?text=DJ+Setlist+AI+-+Main+Interface)
*Main dashboard showing track library and playlist management*

![AI Setlist Generation](https://via.placeholder.com/800x450/1a1a2e/16213e?text=AI+Setlist+Generation)
*AI-powered setlist generation with BPM and harmonic matching*

> **Live Demo**: http://10.93.25.120:3000
> **API Docs**: http://10.93.25.120:8000/docs

---

## 📋 Product Context

### Problem
DJs spend hours manually organizing tracks, matching BPMs, and ensuring harmonic compatibility for seamless transitions. Traditional playlist tools don't understand music theory or DJ-specific requirements.

### Solution
DJ Setlist AI uses artificial intelligence to automatically generate optimized setlists based on:
- **BPM matching** (±5-8 BPM for smooth transitions)
- **Harmonic compatibility** (Camelot Wheel rules for key mixing)
- **Energy progression** (gradual build from 1-10 scale)
- **Genre compatibility**

### Target Users
- **Club DJs**: Prepare setlists for gigs and performances
- **Mobile DJs**: Manage diverse music libraries for events
- **Producers**: Organize reference tracks and plan DJ sets
- **Radio DJs**: Curate shows with smooth transitions

---

## ✨ Features

### ✅ Implemented
- **Music Library Management**: Store tracks with DJ metadata (BPM, musical key, energy level, genre)
- **Playlist Organization**: Create and manage playlists for different occasions
- **AI Setlist Generation**: Qwen AI analyzes tracks and creates optimal ordering
- **Real-time Track Recommendations**: Get AI suggestions for the next track to play
- **Camelot Wheel Integration**: Full support for harmonic mixing notation
- **Interactive API Documentation**: Swagger UI for backend testing
- **Dark-themed DJ Interface**: Designed for low-light performance environments
- **Docker Deployment**: One-command setup with all services
- **Fallback Algorithm**: Automatic fallback if AI generation fails

### 🚧 Planned
- Spotify/Beatport integration for automatic track import
- Real-time audio analysis for BPM/key detection
- Export setlists to popular DJ software (Rekordbox, Serato, Traktor)
- Collaborative playlist sharing
- Mobile-responsive interface
- User authentication and multi-user support
- Setlist history and analytics

---

## 🚀 Usage

### For End Users

1. **Access the Application**:
   - Open your browser and navigate to your server IP on port 3000

2. **Add Tracks**:
   - Go to the "Tracks" page
   - Click "Add Track"
   - Fill in track details:
     - Title, Artist, Genre
     - BPM (beats per minute)
     - Musical Key (Camelot notation, e.g., 8A, 12B)
     - Energy Level (1-10 scale)

3. **Create Playlists**:
   - Navigate to "Playlists"
   - Create a new playlist
   - Add tracks from your library

4. **Generate AI Setlist**:
   - Go to "AI Generator"
   - Select a playlist
   - Configure preferences:
     - Set duration
     - Energy curve (build-up, peak, warm-down)
     - Genre constraints
   - Click "Generate Setlist"
   - Review AI recommendations and adjust if needed

5. **Get Next Track Suggestions**:
   - While performing, use the "Next Track" feature
   - AI will suggest compatible tracks based on what's currently playing

### For Developers

**API Access**:
```bash
# Get all tracks
curl http://localhost:8000/api/tracks/

# Add a new track
curl -X POST http://localhost:8000/api/tracks/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Track Name", "artist": "Artist", "bpm": 128, "key": "8A", "energy": 7}'

# Generate AI setlist
curl -X POST http://localhost:8000/api/ai/generate-setlist \
  -H "Content-Type: application/json" \
  -d '{"playlist_id": 1, "duration_minutes": 60, "energy_curve": "build"}'
```

**Interactive Docs**: Visit http://localhost:8000/docs for full API reference with try-it-out functionality.

---

## 🐳 Deployment

### Target OS
- **Ubuntu 24.04 LTS** (recommended)
- Also compatible with Ubuntu 22.04, Debian 12

### Prerequisites

Before deploying, ensure the following are installed on your VM:

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose (usually comes with Docker)
sudo apt install docker-compose-plugin -y

# Verify installation
docker --version
docker compose version

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker
```

### Step-by-Step Deployment

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/grishaltuhow20182018-create/se-toolkit-hackathon.git
   cd se-toolkit-hackathon
   ```

2. **Configure Environment Variables**:
   ```bash
   # Copy example environment files
   cp backend/.env.example backend/.env

   # Edit backend configuration
   nano backend/.env
   ```

   **Required environment variables** (`backend/.env`):
   ```env
   # Database Configuration
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_secure_password_here
   POSTGRES_DB=djsetlist_db

   # Qwen AI API Configuration
   LLM_API_KEY=your-api-key-here
   LLM_API_BASE_URL=http://your-server-ip:42005/v1
   LLM_API_MODEL=coder-model

   # Server Configuration
   BACKEND_PORT=8000
   FRONTEND_PORT=3000
   POSTGRES_PORT=5432
   PGADMIN_PORT=5050
   ```

3. **Deploy with Docker Compose**:
   ```bash
   # Start all services in background
   docker compose up -d

   # Check service status
   docker compose ps

   # View logs
   docker compose logs -f
   ```

4. **Verify Deployment**:
   ```bash
   # Test backend API
   curl http://localhost:8000/docs

   # Test frontend
   curl http://localhost:3000

   # Check database
   docker compose exec postgres pg_isready -U postgres
   ```

5. **Access the Application**:
   - **Frontend**: http://your-server-ip:3000
   - **Backend API**: http://your-server-ip:8000
   - **API Documentation**: http://your-server-ip:8000/docs
   - **pgAdmin** (database management): http://your-server-ip:5050
     - Email: admin@example.com
     - Password: admin

### Managing the Deployment

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# Restart services
docker compose restart

# View logs
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs -f postgres

# Rebuild after code changes
docker compose up -d --build

# Database backup
docker compose exec postgres pg_dump -U postgres djsetlist_db > backup_$(date +%Y%m%d).sql

# Database restore
docker compose exec -T postgres psql -U postgres djsetlist_db < backup_20250101.sql
```

### Production Considerations

For production deployment, consider:
- **Reverse Proxy**: Set up Nginx or Caddy for SSL/TLS termination
- **Firewall**: Only expose necessary ports (80, 443, 8000)
- **Environment Secrets**: Use Docker secrets or external secret management
- **Database Backups**: Schedule regular automated backups
- **Monitoring**: Set up health checks and alerting
- **Resource Limits**: Configure Docker resource limits in docker-compose.yml

---

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   React     │◄────►│   FastAPI    │◄────►│  PostgreSQL │
│  Frontend   │      │   Backend    │      │  Database   │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                      ┌──────────────┐
                      │  Qwen AI API │
                      │  (LLM Agent) │
                      └──────────────┘
```

### Tech Stack

- **Backend**: FastAPI (Python 3.11), SQLAlchemy (async), Pydantic
- **Frontend**: React 18, Vite, Axios
- **Database**: PostgreSQL 16
- **AI**: Qwen API (OpenAI-compatible)
- **Deployment**: Docker, Docker Compose

---

## 📁 Project Structure

```
se-toolkit-hackathon/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes (tracks, playlists, AI, setlists)
│   │   ├── agents/       # AI agent logic for setlist generation
│   │   ├── core/         # Configuration, database connection
│   │   ├── models/       # SQLAlchemy database models
│   │   ├── schemas/      # Pydantic validation schemas
│   │   └── main.py       # FastAPI application entry point
│   ├── pyproject.toml    # Python dependencies
│   ├── Dockerfile        # Backend container
│   └── .env.example      # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── components/   # Reusable React components
│   │   ├── pages/        # Page components (Tracks, Playlists, AI)
│   │   ├── services/     # API service layer
│   │   └── App.jsx       # Main React component
│   ├── package.json      # Node.js dependencies
│   ├── Dockerfile        # Frontend container
│   └── nginx.conf        # Nginx configuration for production
├── docker-compose.yml    # Multi-service orchestration
├── LICENSE               # MIT License
└── README.md             # This file
```

---

## 🎵 Using Camelot Notation

The app uses Camelot Wheel notation for musical keys:
- **Format**: Number + Letter (e.g., `8A`, `12B`)
- **Compatible keys**: Same number ±1, same letter OR same number, A↔B
- **Example**: 8A mixes well with 7A, 8A, 9A, 8B

### Camelot Wheel Quick Reference
- **8A** → mixes with: 7A, 8A, 9A, 8B
- **12B** → mixes with: 11B, 12B, 1B, 12A

---

## 🤖 AI Agent

The AI agent uses Qwen API with specialized prompts for:

1. **Setlist Generation**: Analyzes all tracks and creates optimal ordering based on BPM, key, energy, and genre
2. **Next Track Recommendation**: Suggests the best next track based on currently playing track
3. **Fallback Algorithm**: If AI fails, uses algorithmic approach (BPM + energy sorting)

---

## 📝 Environment Variables

See `backend/.env.example` for all available configuration options.

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_USER` | Database username | `postgres` |
| `POSTGRES_PASSWORD` | Database password | (required) |
| `POSTGRES_DB` | Database name | `djsetlist_db` |
| `LLM_API_KEY` | Qwen API key | (required) |
| `LLM_API_BASE_URL` | Qwen API endpoint | `http://localhost:42005/v1` |
| `LLM_API_MODEL` | Model to use | `coder-model` |
| `BACKEND_PORT` | Backend port | `8000` |
| `FRONTEND_PORT` | Frontend port | `3000` |

---

## 🐛 Troubleshooting

**Backend can't connect to database**:
```bash
# Check if PostgreSQL is running
docker compose ps

# Verify database connection
docker compose exec postgres pg_isready -U postgres

# Check backend logs
docker compose logs backend
```

**AI generation fails**:
```bash
# Test Qwen API connectivity
curl http://your-server-ip:42005/v1/models

# Verify API key in backend/.env
cat backend/.env | grep LLM_API

# App will automatically fallback to algorithmic mode
```

**Frontend can't reach API**:
```bash
# Ensure backend is running
docker compose ps backend

# Check CORS settings in backend/.env
# FRONTEND_URL should match your frontend URL
```

**Port conflicts**:
```bash
# Check if ports are already in use
sudo lsof -i :8000
sudo lsof -i :3000
sudo lsof -i :5432

# Change ports in docker-compose.yml and backend/.env
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (when available)
5. Commit your changes (`git commit -m 'Add amazing feature

Co-authored-by: Qwen-Coder <qwen-coder@alibabacloud.com>'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🎉 Credits

Built with ❤️ for DJs, producers, and music enthusiasts.

**AI powered by**: [Qwen API](https://qwen.ai)

**Tech Stack**:
- FastAPI - Modern Python web framework
- React - Component-based UI library
- PostgreSQL - Robust relational database
- Docker - Container orchestration

---

## 📊 Repository & Deployment Links

**GitHub Repository**: https://github.com/grishaltuhow20182018-create/se-toolkit-hackathon

**Live Deployment**: http://10.93.25.120:3000

**API Documentation**: http://10.93.25.120:8000/docs

---

*Made for the SE Toolkit Hackathon 2025*
