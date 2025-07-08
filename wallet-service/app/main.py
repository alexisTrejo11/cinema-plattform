
from fastapi import FastAPI
from app.interfaces.api.routers import wallets, users
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Wallet Service API",
    description="API for managing wallets and users.",
    version="1.0.0",
)

app.include_router(wallets.router, prefix="/wallets", tags=["wallets"])
app.include_router(users.router, prefix="/users", tags=["users"])

