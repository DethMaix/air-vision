from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from app.api.v1.routes.health import router as health_router
from app.api.v1.routes.reg import router as reg_router

# Exception handlers
from app.api.errors import register_exception_handlers


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
app.include_router(health_router, prefix="/v1/health")
app.include_router(reg_router, prefix="/v1/reg")

# Register exception handlers
register_exception_handlers(app)

# Main endpoint [temp]
@app.get("/")
async def root() -> dict:
    return {"Hello": "World"}
