from fastapi import FastAPI
from app.food.infrastructure.api import category_controller, food_controller

app = FastAPI(
    title="Cinema Backend: Food Service API",
    debug=True,
    summary="Food Service for Cinema API that includes all food catalog and combos offers and all related to food directly",
    version="1.0.0"
)


@app.get("/ping")
def ping():
    return "pong"

app.include_router(category_controller.router)
app.include_router(food_controller.router)