from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ai_service import ai_service
from app.schemas.food import FoodScanResponse

router = APIRouter()

@router.post("/scan", response_model=FoodScanResponse)
async def scan_food(file: UploadFile = File(...)):
    # Validar formatos de imagen comunes de dispositivos móviles
    allowed_types = ["image/jpeg", "image/png", "image/webp", "image/heic", "image/heif"]
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail=f"Formato de archivo no soportado ({file.content_type}). Por favor sube una imagen (JPEG, PNG, WEBP o HEIC)."
        )
    
    contents = await file.read()
    result = await ai_service.scan_food_image(contents)
    return result
