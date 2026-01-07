from pydantic import BaseModel
from typing import List, Optional

class FoodItemDetection(BaseModel):
    name: str
    calories: float
    protein: float
    carbs: float
    fats: float
    unit: str = "portion"
    amount: float = 1.0

class FoodScanResponse(BaseModel):
    detected_food: List[FoodItemDetection]
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fats: float
    confidence: float
    note: Optional[str] = None
