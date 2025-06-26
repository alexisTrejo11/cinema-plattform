from fastapi import FastAPI

app = FastAPI(
    title="Cinema Backend: Food Service API",
    debug=True,
    summary="Food Service for Cinema API that includes all food catalog and combos offers and all related to food directly",
    version="1.0.0"
)



@app.get("/ping")
def ping():
    return "pong"