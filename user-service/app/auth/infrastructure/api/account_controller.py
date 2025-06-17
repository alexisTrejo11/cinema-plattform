from fastapi import APIRouter
from app.users.domain.entities import User


app = APIRouter(prefix="/api/v1/accounts")

@app.get("/", response_model=User)
def send_activate_token(user: User):
    return user


@app.get("/", response_model=User)
def activate_account(user: User):
    return user


@app.get("/", response_model=User)
def deactivate_account(user: User):
    return user


@app.get("/", response_model=User)
def delete_account(user: User):
    return user