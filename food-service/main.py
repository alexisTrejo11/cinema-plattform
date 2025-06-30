from fastapi import FastAPI
from app.products.infrastructure.api import category_controller, food_controller
from app.combos.infrastructure.api import combo_controllers
from config.model_init import *
from config import exception_handlers

app = FastAPI(
    title="Cinema Backend: Food Service API",
    debug=True,
    summary="Food Service for Cinema API that includes all food catalog and combos offers and all related to food directly",
    version="1.0.0",
    exception_handlers=exception_handlers
)

@app.get("/ping")
def ping():
    return "pong"

app.include_router(category_controller.router)
app.include_router(food_controller.router)
app.include_router(combo_controllers.router)