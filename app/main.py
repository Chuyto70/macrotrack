from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.schemas.error import ErrorResponse, APIError
from app.api.api_v1.api import api_router
from app.core.config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global exception: {exc}", exc_info=True)
    
    # Manejar errores específicos de Google API si es posible sin importar directamente
    # por si no está instalado o tiene otro nombre en tiempo de ejecución
    exc_name = type(exc).__name__
    
    if "InvalidArgument" in exc_name or "API key not valid" in str(exc):
        return JSONResponse(
            status_code=401,
            content=ErrorResponse(
                success=False,
                error=APIError(
                    code="INVALID_API_KEY",
                    message="La configuración del servidor es incorrecta (API Key de IA inválida).",
                    detail=str(exc) if settings.VERSION == "0.1.0" else None
                )
            ).model_dump()
        )

    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            success=False,
            error=APIError(
                code="INTERNAL_SERVER_ERROR",
                message="Ha ocurrido un error inesperado en el servidor.",
                detail=str(exc) if settings.VERSION == "0.1.0" else None
            )
        ).model_dump()
    )

@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=404,
        content=ErrorResponse(
            success=False,
            error=APIError(
                code="NOT_FOUND",
                message="El recurso solicitado no existe."
            )
        ).model_dump()
    )

from fastapi import HTTPException
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            success=False,
            error=APIError(
                code="HTTP_ERROR",
                message=str(exc.detail)
            )
        ).model_dump()
    )

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite peticiones de cualquier lugar (ideal para desarrollo y apps móviles)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Welcome to MacroTrack API", "docs": "/docs"}
