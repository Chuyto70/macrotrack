from pydantic import BaseModel
from typing import Optional

class UserStats(BaseModel):
    weight: float
    height: float
    age: int
    gender: str # 'male' or 'female'
    activity_level: str # 'sedentary', 'lightly_active', 'moderately_active', 'very_active', 'extra_active'
    goal: str # 'lose_weight', 'gain_muscle', 'maintain'

class NutrientResults(BaseModel):
    bmr: float
    tdee: float
    target_calories: float
    protein: float
    carbs: float
    fats: float
