"""OpenAPI fragments shared by wallet routes."""

common_wallet_error_responses = {
    "401": {"description": "Unauthorized — missing or invalid JWT."},
    "403": {"description": "Forbidden — insufficient role or scope."},
    "404": {"description": "Wallet or related resource not found."},
    "422": {"description": "Validation error on request body or parameters."},
    "429": {"description": "Rate limit exceeded."},
    "500": {"description": "Internal server error."},
}
