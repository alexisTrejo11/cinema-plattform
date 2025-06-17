from fastapi import APIRouter
from app.users.domain.entities import User


app = APIRouter(prefix="/api/v1/profiles")

@app.get("/", response_model=User)
def get_my_profile(user: User):
    return user


@app.patch("/")
def update_my_profile(user: User):
    return user


