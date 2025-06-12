from fastapi import FastAPI, Request

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

from model_initialization import *
from config import exception_handlers
from app.shared import logging

from app.movies.infrastructure.api import movie_controllers
from app.movies.infrastructure.api import movie_showtime_controller
from app.cinema.infrastructure.api import cinema_controllers
from app.theater.infrastructure.api import theater_controllers, theather_seat_controllers
from app.showtime.infrastructure.api import showtime_controller

logging.setup_logging()

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
        title="Cinema Backend: Billboard Service API",
        version="1.0.0",
        exception_handlers=exception_handlers
    )

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.get("/")
@limiter.limit("5/minute")  # type: ignore
def read_home(request: Request):
    return { "home": "Welcome To Billboard Service" } 

app.include_router(movie_controllers.router)
app.include_router(movie_showtime_controller.router)

app.include_router(cinema_controllers.router)

app.include_router(theater_controllers.router)
app.include_router(theather_seat_controllers.router)

app.include_router(showtime_controller.router)
