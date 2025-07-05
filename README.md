# Ranked Choice Voting Application

A web application for conducting and managing ranked choice voting polls, built with Django and React TypeScript.

## Project Structure

```
ranked-choice/
├── backend/               # Django backend
│   ├── ranked_choice/     # Django project
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Core functionality
│   │   ├── settings.py    # Django settings
│   │   └── ...
│   ├── templates/         # Django templates
│   ├── static/            # Static files
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile         # Backend Dockerfile
├── frontend/              # React TypeScript frontend
│   ├── src/               # Source code
│   │   ├── components/    # Reusable components
│   │   ├── pages/         # Page components
│   │   └── services/      # API services
│   ├── public/            # Static assets
│   ├── package.json       # Node.js dependencies
│   └── Dockerfile         # Frontend Dockerfile
├── docker-compose.yml     # Docker Compose configuration
└── .env.example           # Example environment variables
```

## Prerequisites

- Docker and Docker Compose
- Git

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ranked-choice.git
   cd ranked-choice
   ```

2. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

3. Start the application with Docker Compose:
   ```bash
   docker compose up -d
   ```

4. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000/api/
   - Django Admin: http://localhost:8000/admin/

## Development

### Backend (Django)

- The Django application is in the `backend/` directory
- API endpoints are defined in `backend/ranked_choice/api/`
- Core functionality is in `backend/ranked_choice/core/`

### Frontend (React TypeScript)

- The React application is in the `frontend/` directory
- Components are in `frontend/src/components/`
- Pages are in `frontend/src/pages/`
- API services are in `frontend/src/services/`

## Deployment

For production deployment:

1. Update the `.env` file with production settings:
   - Set `DEBUG=False`
   - Set a strong `SECRET_KEY`
   - Update `ALLOWED_HOSTS` and `CORS_ALLOWED_ORIGINS`

2. Build and run the Docker containers:
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
   ```

## License

[MIT License](LICENSE)
