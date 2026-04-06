"""
Middleware module for the shared package.

This module contains the middleware functions that are used across all the microservices.

It includes:
- Jwt Auth Security
- Logging

The goal is to provide a consistent approach to the development of the microservices
to follow a consistent approach to the development of the microservices.

Requires Pydantic v2, PyJWT, and FastAPI.
"""

from .jwt_security import jwt_auth_middleware
from .logging import logging_middleware