# Ranked Choice Voting Application
#### Video Demo: https://www.youtube.com/watch?v=b-oapnCuKEo
#### Description:

A web application for conducting and managing ranked choice voting polls, built with Python (Django), and React TypeScript.
Persistence is run with PostGreSQL and the app is run in Docker Containers. Four GitHub actions are included that run lint
and test checks for both code bases. 

Create a ballot, collect votes, and display results. Results of ballots highlight the rounds calculated when tallying votes.

## Project Structure

```
ranked-choice/
├── backend/               # Django backend
│   ├── ranked_choice/     # Django project
│   │   ├── api/           # API endpoints
│   │   ├── core/          # Core functionality
│   │   ├── tests/         # integration & unit tests
│   │   ├── settings.py    # Django settings
│   │   └── ...
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile         # Backend Dockerfile
├── frontend/              # React TypeScript frontend
│   ├── src/               # Source code
│   │   ├── components/    # Reusable components
│   │   ├── pages/         # Page components
│   │   └── services/      # API services
│   │   └── styles/        # css styles
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
   make build && make start
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

### Linting

The project uses [Ruff](https://github.com/astral-sh/ruff) for Python linting.

To run the linter locally:
```bash
make lint
```

To automatically fix linting issues:
```bash
make lint-fix
```

For frontend TypeScript files we use ESLint

To automatically fix (most) linting issues:
```bash
make lint-ui
```

### Testing
For backend tests run:
```bash
make test
```

For frontend tests run:
```bash
make test-ui
```

The project also includes a GitHub Actions workflow that automatically runs the linter on all pull requests and pushes to the main branch.

#### Configuring PyCharm for Ruff

To configure PyCharm to use Ruff for linting on save:

1. Install the Ruff plugin:
   - Go to Settings/Preferences → Plugins
   - Search for "Ruff" and install the plugin
   - Restart PyCharm

2. Configure the Ruff plugin:
   - Go to Settings/Preferences → Tools → Ruff
   - Check "Run on save"
   - Set the path to the Ruff executable (usually in your virtual environment)
   - Click "Apply" and "OK"

3. Verify the configuration:
   - Open a Python file
   - Make a change that would trigger a linting error
   - Save the file and verify that Ruff highlights the issue

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
