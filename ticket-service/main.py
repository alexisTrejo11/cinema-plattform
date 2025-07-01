from fastapi import FastAPI

app = FastAPI(
    debug=True, 
    version="2.0.0",
    title="CINEMA API: Ticket Service",
    summary="Microservice that manages tickets operation for showtimes"
    )


@app.get("/health")
def health_check():
        return {"status": "healthy", "service": "ticket-service"}

    
    
