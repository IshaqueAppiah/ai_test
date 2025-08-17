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
│   ├── app.py              # FastAPI server with chat endpoint
│   └── requirements.txt    # Python dependencies
├── frontend/
│   └── index.html         # Chat interface
├── Dockerfile.backend     # Backend container
├── Dockerfile.frontend    # Frontend container
├── docker-compose.yml     # Container orchestration
└── CURRICULUM.md          # Course details
```

Students progressively enhance the single `/chat` endpoint each week, adding capabilities like streaming, memory, RAG, function calling, and production features.

**📋 [View complete curriculum →](CURRICULUM.md)**