from app.shared.documentation import (
    common_wallet_error_responses as common_error_responses,
)

walleyByIdDoc = {
    "summary": "Retrieve Wallet by ID",
    "description": """
    Retrieves detailed information for a specific wallet using its unique identifier.

    This endpoint requires authentication as an employee.
    It can optionally include a list of recent transactions associated with the wallet.
    """,
    "responses": {
        **common_error_responses,
        "200": {
            "description": "Wallet successfully retrieved.",
            "content": {
                "application/json": {
                    "examples": {
                        "success": {
                            "summary": "Successful Wallet Retrieval",
                            "value": {
                                "message": "Wallet Successfully Retrieved",
                                "data": {
                                    "id": "b1c2d3e4-f5a6-7890-1234-567890abcdef",
                                    "user_id": "1a2b3c4d-5e6f-7890-1234-567890abcdef",
                                    "balance": {"amount": 1250.75, "currency": "USD"},
                                    "transactions": [],  # Example with no transactions
                                },
                                "error": None,
                            },
                        }
                    }
                }
            },
        },
    },
}


walleyByUserIdDoc = {
    "summary": "Retrieve Wallet by ID",
    "description": """
    Retrieves detailed information for a specific wallet associated with a user ID.

    This endpoint requires authentication as an employee.
    It can optionally include a list of recent transactions for the wallet.
    """,
    "responses": {
        **common_error_responses,
        200: {
            "description": "Wallet successfully retrieved.",
            "content": {
                "application/json": {
                    "examples": {
                        "success": {
                            "summary": "Successful Wallet Retrieval by User ID",
                            "value": {
                                "message": "Wallet Successfully Retrieved",
                                "data": {
                                    "id": "b1c2d3e4-f5a6-7890-1234-567890abcdef",
                                    "user_id": "1a2b3c4d-5e6f-7890-1234-567890abcdef",
                                    "balance": {"amount": 1250.75, "currency": "USD"},
                                    "transactions": [],  # Example with no transactions
                                },
                                "error": None,
                            },
                        }
                    }
                }
            },
        },
    },
}


addCreditDoc = {
    "summary": "Add Credit to a Wallet",
    "description": """
    Adds a specified amount of credit to a wallet. This operation typically represents
    a top-up or a deposit into the user's wallet.

    This endpoint requires authentication as an employee.
    The `WalletOperationRequest` includes the target wallet ID, amount, currency,
    and details of the payment used for the credit addition.
    """,
    "responses": {
        **common_error_responses,
        200: {
            "description": "Credit successfully added to the wallet.",
            "content": {
                "application/json": {
                    "examples": {
                        "success": {
                            "summary": "Successful Credit Addition",
                            "value": {
                                "message": "Credit Recharge Successfully processed in wallet",
                                "data": {
                                    "id": "b1c2d3e4-f5a6-7890-1234-567890abcdef",
                                    "user_id": "1a2b3c4d-5e6f-7890-1234-567890abcdef",
                                    "balance": 1300.75,  # Example new balance
                                    "transaction": {
                                        "transaction_id": "g1h2i3j4-k5l6-7890-1234-567890abcdef",
                                        "wallet_id": "b1c2d3e4-f5a6-7890-1234-567890abcdef",
                                        "amount": {"amount": 50.00, "currency": "USD"},
                                        "transaction_type": "CREDIT",
                                        "payment_details": {
                                            "payment_method": "card",
                                            "payment_id": "x1y2z3a4-b5c6-7890-1234-567890abcdef",
                                        },
                                        "timestamp": "2024-07-15T19:30:00.123456Z",
                                    },
                                },
                                "error": None,
                            },
                        }
                    }
                }
            },
        },
    },
}


payCartDoc = {
    "summary": "Make a Payment from a Wallet",
    "description": """
    Initiates a payment from a specified wallet, debiting the given amount.

    This endpoint requires authentication as an employee.
    The `WalletOperationRequest` includes the wallet ID, amount, currency,
    and details of the payment being made.
    """,
    "responses": {
        **common_error_responses,
        200: {
            "description": "Payment successfully processed from the wallet.",
            "content": {
                "application/json": {
                    "examples": {
                        "success": {
                            "summary": "Successful Payment",
                            "value": {
                                "message": "Pay Successfully processed in wallet",
                                "data": {
                                    "id": "b1c2d3e4-f5a6-7890-1234-567890abcdef",
                                    "user_id": "1a2b3c4d-5e6f-7890-1234-567890abcdef",
                                    "balance": 1200.00,  # Example new balance after payment
                                    "transaction": {
                                        "transaction_id": "h1i2j3k4-l5m6-7890-0123-456789abcdef",
                                        "wallet_id": "b1c2d3e4-f5a6-7890-1234-567890abcdef",
                                        "amount": {"amount": 100.75, "currency": "USD"},
                                        "transaction_type": "DEBIT",
                                        "payment_details": {
                                            "payment_method": "merchant_purchase",
                                            "payment_id": "y1z2a3b4-c5d6-7890-1234-567890abcdef",
                                        },
                                        "timestamp": "2024-07-15T19:45:00.123456Z",
                                    },
                                },
                                "error": None,
                            },
                        }
                    }
                }
            },
        },
    },
}
