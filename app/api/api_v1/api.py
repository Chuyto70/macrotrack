from fastapi import APIRouter
from app.api.api_v1.endpoints import calculator, food

api_router = APIRouter()
api_router.include_router(calculator.router, prefix="/calculator", tags=["calculator"])
api_router.include_router(food.router, prefix="/food", tags=["food"])
