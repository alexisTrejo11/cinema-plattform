from fastapi import FastAPI, Request

app = FastAPI(
    title="Cinema Backend: User Service API",
    version="1.0.0"
    )

@app.get("/home/")
def home(request: Request): 
    return {"home" : "Welcome to User Service" }
