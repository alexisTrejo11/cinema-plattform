from fastapi import FastAPI, status
from app.user.presentation import user_admin_controller

app = FastAPI()


@app.get("/ping", status_code=status.HTTP_200_OK)
async def ping():
    return {"message": "pong"}


@app.get("/health", status_code=status.HTTP_200_OK)
async def health():
    return {"status": "ok"}


app.include_router(user_admin_controller.router)
