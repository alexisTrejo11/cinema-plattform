from fastapi import FastAPI

app = FastAPI()

@app.get("/ping")
def ping():
    return {"ping": "pong"}

@app.get("/health")
def health():
    return {"status": "ok"}

