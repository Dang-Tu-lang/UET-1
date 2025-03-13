from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware
from config import app_config 

from starlette.responses import JSONResponse
API_KEY = app_config.api_key
API_KEY_NAME = "api-key"



PROTECTED_ROUTES = ["/alert-matching/"]  # Chỉ áp dụng auth cho các route này

class APIKeyMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path.rstrip("/")
        if path in PROTECTED_ROUTES:
            api_key = request.headers.get(API_KEY_NAME)
            if api_key != API_KEY:
                return JSONResponse(
                    status_code=403,
                    content={"error": "Invalid API Key", "message": "You are not authorized to access this resource"}
                )
        
        response = await call_next(request)
        return response

async def startup_hook(app: FastAPI):
    logger.info("Starting up...")


async def shutdown_hook(app: FastAPI):
    logger.info("Shutting down...")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup_hook(app)

    from api.routers import router

    app.include_router(router)
    yield
    await shutdown_hook(app)

# get_api_key()
app = FastAPI(
    title=app_config.name,
    description="""Alert Matching""",
    lifespan=lifespan,
)
from api.routers import router
app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(APIKeyMiddleware)
if __name__ == "__main__":
    uvicorn.run("main:app", host=app_config.host, port=app_config.port, workers=app_config.workers)
