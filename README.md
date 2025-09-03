# AI Application Developer Labs

A 10-week learning journey building AI applications incrementally. This repository provides the foundational structure that students build upon week by week.

**📋 [CURRICULUM.md](CURRICULUM.md)** - Complete course details and weekly schedule

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Git

### Running the Application

1. Start the application:
```bash
docker-compose up --build -d
```

2. Access the application:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### Stopping the Application
```bash
docker-compose down
```

## Development

### Project Structure
```
├── backend/
│   ├── app.py              # Backend: FastAPI server with chat endpoint
│   ├── pyproject.toml      # Backend: Python dependencies and config
│   └── tests/              # Backend: Test suite
│       └── ...
├── frontend/
│   └── index.html         # Frontend: Chat interface
├── Dockerfile.backend     # Ops: Backend container
├── Dockerfile.frontend    # Ops: Frontend container
├── docker-compose.yml     # Ops: Container orchestration
└── CURRICULUM.md          # Docs: Course details
```

### Backend Development

**Prerequisites:** 
- [uv](https://docs.astral.sh/uv/) installed for Python development

**Development Workflow:**
```bash
# Install dependencies
cd backend && uv sync

# Run server locally for development
cd backend && uv run uvicorn app:app --reload

# Run tests
cd backend && uv run pytest tests/ -v

# Run specific week tests
cd backend && uv run pytest tests/test_week_01.py -v

# Run only unit tests (skip external / metered API calls)
cd backend && uv run pytest tests/ -v -m "not integration"
```

**📋 [View complete curriculum →](CURRICULUM.md)**