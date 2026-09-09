# Air Vision Server

Backend API for the Air Vision project.

## Future Documentation Template

> Keep this section up to date as the server grows.

### Overview

<!-- Describe the server's responsibilities and its role in the project. -->

### Requirements

<!-- List Python, database, service, and environment requirements. -->

### Setup

<!-- Document installation and environment setup steps. -->

### Running Locally

<!-- Document the development server command and available local URLs. -->

### Configuration

<!-- Document environment variables and configuration files. -->

### API

<!-- Link to or summarize the available API endpoints. -->

### Project Structure

<!-- Keep the annotated tree below synchronized with the codebase. -->

### Testing

<!-- Document the test command and important test conventions. -->

### Deployment

<!-- Document build, deployment, and production operation steps. -->

## Current Structure

```text
server/
├── README.md                         # Server documentation and project guide
├── pyproject.toml                    # Python project metadata and dependencies
├── .gitignore                        # Files excluded from version control
└── app/
    ├── __init__.py                   # Marks app as a Python package
    ├── main.py                       # Creates the FastAPI app, CORS, and root endpoint
    ├── api/
    │   ├── __init__.py               # Marks the API package
    │   └── v1/
    │       ├── __init__.py           # Marks the version 1 API package
    │       └── routes/
    │           ├── __init__.py       # Marks the routes package
    │           └── health.py         # Defines the /health health-check endpoint
    └── domains/
        ├── __init__.py               # Marks the domain package
        └── flights/
            └── __init__.py           # Placeholder for flight-domain logic
```

The local `.venv/` directory may also exist under `server/`; it contains the local Python environment and is intentionally not tracked.

## Current API

- `GET /` returns a temporary greeting response.
- `GET /health` returns the service status.

The FastAPI application is defined in `app/main.py`.
