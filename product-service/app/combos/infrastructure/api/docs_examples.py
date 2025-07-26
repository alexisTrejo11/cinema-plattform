from app.shared.docs.common_responses import (
    common_error_responses,
    common_public_error_responses,
)
from fastapi import status


create_combo_examples = {
    **common_error_responses,
    status.HTTP_201_CREATED: {
        "description": "Combo created successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "data": {
                        "id": "c7cdc31d-6682-418a-b9ca-df13a3e85da5 ",
                        "name": "Family Combo",
                        "description": "A large combo for the whole family",
                        "items": [
                            {
                                "product_id": "c7cdc31d-6682-418a-b9ca-df13a3e85da5 ",
                                "quantity": 2,
                            },
                            {
                                "product_id": "c7cdc31d-6682-418a-b9ca-df13a3e85da5 ",
                                "quantity": 1,
                            },
                        ],
                        "price": 29.99,
                        "image_url": "https://example.com/combo.jpg",
                        "is_available": True,
                        "discount_percentage": 10,
                    },
                    "error": None,
                    "message": "Combo created successfully",
                    "timestamp": "2023-10-01T12:00:00Z",
                }
            }
        },
    },
}

get_combo_examples = {
    **common_public_error_responses,
    status.HTTP_200_OK: {
        "description": "Combo retrieved successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "data": {
                        "id": "c7cdc31d-6682-418a-b9ca-df13a3e85da5 ",
                        "name": "Family Combo",
                        "description": "A large combo for the whole family",
                        "items": [
                            {
                                "product_id": "c7cdc31d-6682-418a-b9ca-df13a3e85da5 ",
                                "quantity": 2,
                            },
                            {
                                "product_id": "c7cdc31d-6682-418a-b9ca-df13a3e85da5 ",
                                "quantity": 1,
                            },
                        ],
                        "price": 29.99,
                        "image_url": "https://example.com/combo.jpg",
                        "is_available": True,
                        "discount_percentage": 10,
                    },
                    "error": None,
                    "message": "Combo retrieved successfully",
                    "timestamp": "2023-10-01T12:00:00Z",
                }
            }
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Combo not found",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "data": None,
                    "error": "Combo not found",
                    "message": "The requested combo does not exist",
                    "timestamp": "2023-10-01T12:00:00Z",
                }
            }
        },
    },
}

list_combos_examples = {
    **common_public_error_responses,
    status.HTTP_200_OK: {
        "description": "Combos retrieved successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "data": [
                        {
                            "id": "c7cdc31d-6682-418a-b9ca-df13a3e85da5 ",
                            "name": "Family Combo",
                            "description": "A large combo for the whole family",
                            "items": [
                                {
                                    "product_id": "c7cdc31d-6682-418a-b9ca-df13a3e85da5 ",
                                    "quantity": 2,
                                },
                                {
                                    "product_id": "c7cdc31d-6682-418a-b9ca-df13a3e85da5 ",
                                    "quantity": 1,
                                },
                            ],
                            "price": 29.99,
                            "image_url": "https://example.com/combo.jpg",
                            "is_available": True,
                            "discount_percentage": 10,
                        }
                    ],
                    "error": None,
                    "message": "Combos retrieved successfully",
                    "timestamp": "2023-10-01T12:00:00Z",
                }
            }
        },
    },
}


update_combo_examples = {
    **common_error_responses,
    status.HTTP_200_OK: {
        "description": "Combo updated successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "data": {
                        "id": "c7cdc31d-6682-418a-b9ca-df13a3e85da5 ",
                        "name": "Updated Family Combo",
                        "description": "An updated large combo for the whole family",
                        "items": [
                            {
                                "product_id": "c7cdc31d-6682-418a-b9ca-df13a3e85da5 ",
                                "quantity": 3,
                            },
                            {
                                "product_id": "c7cdc31d-6682-418a-b9ca-df13a3e85da5 ",
                                "quantity": 1,
                            },
                        ],
                        "price": 34.99,
                        "image_url": "https://example.com/updated_combo.jpg",
                        "is_available": True,
                        "discount_percentage": 15,
                    },
                }
            }
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Combo not found",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "data": None,
                    "error": "Combo not found",
                    "message": "The requested combo does not exist",
                    "timestamp": "2023-10-01T12:00:00Z",
                }
            }
        },
    },
}


delete_combo_examples = {
    **common_error_responses,
    status.HTTP_200_OK: {
        "description": "Combo deleted successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "data": None,
                    "error": None,
                    "message": "Combo deleted successfully",
                    "timestamp": "2023-10-01T12:00:00Z",
                }
            }
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Combo not found",
        "content": {
            "application/json": {
                "example": {
                    "success": False,
                    "data": None,
                    "error": "Combo not found",
                    "message": "The requested combo does not exist",
                    "timestamp": "2023-10-01T12:00:00Z",
                }
            }
        },
    },
}
