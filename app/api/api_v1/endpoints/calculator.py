from fastapi import APIRouter
from app.schemas.calculator import UserStats, NutrientResults

router = APIRouter()

@router.post("/calculate-macros", response_model=NutrientResults)
def calculate_macros(stats: UserStats):
    # Mifflin-St Jeor Formula
    if stats.gender.lower() == "male":
        bmr = (10 * stats.weight) + (6.25 * stats.height) - (5 * stats.age) + 5
    else:
        bmr = (10 * stats.weight) + (6.25 * stats.height) - (5 * stats.age) - 161
    
    # Activity Factors
    activity_factors = {
        "sedentary": 1.2,
        "lightly_active": 1.375,
        "moderately_active": 1.55,
        "very_active": 1.725,
        "extra_active": 1.9
    }
    
    factor = activity_factors.get(stats.activity_level.lower(), 1.2)
    tdee = bmr * factor
    
    # Goal adjustments (simplified)
    target_calories = tdee
    if stats.goal == "lose_weight":
        target_calories = tdee - 500
    elif stats.goal == "gain_muscle":
        target_calories = tdee + 300
    
    # Macro Distributions
    # Perder Peso: P:35%, C:35%, G:30%
    # Ganar Músculo: P:30%, C:45%, G:25%
    # Mantener: P:30%, C:40%, G:30%
    
    if stats.goal == "lose_weight":
        p_ratio, c_ratio, f_ratio = 0.35, 0.35, 0.30
    elif stats.goal == "gain_muscle":
        p_ratio, c_ratio, f_ratio = 0.30, 0.45, 0.25
    else:
        p_ratio, c_ratio, f_ratio = 0.30, 0.40, 0.30
        
    # Grams: Protein 4cal/g, Carbs 4cal/g, Fats 9cal/g
    protein = (target_calories * p_ratio) / 4
    carbs = (target_calories * c_ratio) / 4
    fats = (target_calories * f_ratio) / 9
    
    return {
        "bmr": round(bmr, 2),
        "tdee": round(tdee, 2),
        "target_calories": round(target_calories, 2),
        "protein": round(protein, 1),
        "carbs": round(carbs, 1),
        "fats": round(fats, 1)
    }
