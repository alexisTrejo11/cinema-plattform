"""
Middleware module for the shared package.

This module contains the middleware functions that are used across all the microservices.

It includes:
- JWT auth (optional Bearer token)
- Logging

The goal is to provide a consistent app.ach to the development of the microservices
to follow a consistent app.ach to the development of the microservices.

Requires Pydantic v2, PyJWT, and FastAPI.
"""

from .jwt_security import JwtAuthMiddleware
from .logging_middleware import LoggingMiddleware


__all__ = ["JwtAuthMiddleware", "LoggingMiddleware"]
