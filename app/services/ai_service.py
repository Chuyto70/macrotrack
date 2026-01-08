import json
import io
import logging
from PIL import Image
from fastapi import HTTPException
from google import genai
from app.core.config import settings
from app.schemas.food import FoodScanResponse, FoodItemDetection

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):

        if settings.GOOGLE_API_KEY:
            # Nueva SDK: google-genai
            self.client = genai.Client(api_key=settings.GOOGLE_API_KEY)
            self.model = 'gemini-3-flash-preview'
        else:
            self.client = None

    async def scan_food_image(self, image_bytes: bytes) -> FoodScanResponse:
        if not self.client:
            # Mock response if no API key is set
            return self._get_mock_response()

        try:
            image = Image.open(io.BytesIO(image_bytes))
            # Verificar que sea realmente una imagen intentando cargar los datos
            image.verify()
            # La mayoría de las veces image.verify() cierra el archivo, 
            # así que lo reabrimos para estar seguros
            image = Image.open(io.BytesIO(image_bytes))
        except Exception as e:
            logger.error(f"Error opening image: {e}")
            raise HTTPException(
                status_code=400,
                detail="El contenido del archivo no es una imagen válida o está corrupto."
            )
        
        prompt = """
        Analyze this food image and provide a nutritional breakdown in JSON format.
        Include 'detected_food' as a list of items, each with 'name', 'calories', 'protein', 'carbs', 'fats', 'unit', and 'amount'.
        Also include 'total_calories', 'total_protein', 'total_carbs', 'total_fats', and a 'confidence' score (0.0 to 1.0).
        If multiple items are found, list them all.
        The output must be ONLY the JSON string.
        """

        try:
            # Llamada con la nueva SDK
            response = self.client.models.generate_content(
                model=self.model,
                contents=[prompt, image]
            )
        except Exception as e:
            logger.error(f"Gemini API Error: {e}")
            raise e
        
        try:
            # En la nueva SDK, el acceso es similar .text
            text = response.text
            
            # Limpieza de markdown si es necesario
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            
            data = json.loads(text)
            return FoodScanResponse(**data)
        except Exception as e:
            logger.error(f"Error parsing Gemini response: {e}")
            return self._get_mock_response()

    def _get_mock_response(self) -> FoodScanResponse:
        return FoodScanResponse(
            detected_food=[
                FoodItemDetection(
                    name="Ensalada Caesar (Mock)",
                    calories=350,
                    protein=15.5,
                    carbs=12.0,
                    fats=25.0,
                    unit="plato",
                    amount=1.0
                )
            ],
            total_calories=350,
            total_protein=15.5,
            total_carbs=12.0,
            total_fats=25.0,
            confidence=0.9,
            note="Este es un resultado de prueba (Nueva SDK). Configura GOOGLE_API_KEY correctamente."
        )

ai_service = AIService()
