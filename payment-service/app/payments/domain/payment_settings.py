"""
Payment domain configuration loaded from the environment.

Expiry and similar values can differ by environment or deployment.
"""

import os

PAYMENT_EXPIRY_MINUTES = int(os.getenv("PAYMENT_EXPIRY_MINUTES", "30"))
