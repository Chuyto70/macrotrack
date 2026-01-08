from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ai_service import ai_service
from app.schemas.food import FoodScanResponse

router = APIRouter()

@router.post("/scan", response_model=FoodScanResponse)
async def scan_food(file: UploadFile = File(...)):
    # Validar formatos de imagen comunes de dispositivos móviles
    # A veces los móviles envían 'application/octet-stream', por lo que permitimos ese tipo
    # y dejamos que PIL verifique si realmente es una imagen válida.
    allowed_types = [
        "image/jpeg", "image/png", "image/webp", "image/heic", "image/heif",
        "application/octet-stream"
    ]
    
    if file.content_type not in allowed_types and not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400, 
            detail=f"Formato de archivo no soportado ({file.content_type}). Por favor sube una imagen válida."
        )
    
    contents = await file.read()
    result = await ai_service.scan_food_image(contents)
    return result
