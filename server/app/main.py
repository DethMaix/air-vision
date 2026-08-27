from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from api.v1.routes.health import router as health_router

# App initialization
app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers include
app.include_router(health_router)

# Main endpoint [temp]
@app.get('/')
def root() -> dict:
    return {"Hello": "World"}
