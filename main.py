from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.models import User, Role

from app.routes import auth_routes, user_routes, firebase_routes
from app.middleware.cors import setup_cors
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.exceptions.handlers import (
    validation_exception_handler,
    sqlalchemy_exception_handler,
    integrity_exception_handler,
    general_exception_handler,
)

# Uncomment when Firebase is configured:
# from app.utils.firebase_auth import initialize_firebase

app = FastAPI(
    title="FastAPI MVC Application",
    description="FastAPI with MySQL/MariaDB and Firebase Auth",
    version="1.0.0",
)

# Setup CORS middleware
setup_cors(app)

# Register exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)  # type: ignore
app.add_exception_handler(IntegrityError, integrity_exception_handler)  # type: ignore
app.add_exception_handler(Exception, general_exception_handler)  # type: ignore

# Register routers
app.include_router(auth_routes.router, prefix="/api")
app.include_router(user_routes.router, prefix="/api")
app.include_router(firebase_routes.router, prefix="/api")


# Uncomment when Firebase is configured:
# @app.on_event("startup")
# async def startup_event():
#     """Initialize services on application startup"""
#     initialize_firebase()
#     print("Application startup complete")


@app.get("/")
async def root():
    return {"message": "Hello World", "status": "running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/test")
async def test():
    return JSONResponse(
        content={
            "message": "FastAPI is working!",
            "endpoints": ["/", "/health", "/docs", "/redoc"],
        }
    )


# Run with: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
