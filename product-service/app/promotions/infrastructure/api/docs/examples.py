from app.shared.docs.common_responses import common_error_responses as common_responses
from fastapi import status

create_promotion_examples = {
    "201": {
        "description": "Promotion created successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "Promotion created successfully.",
                    "data": {"id": "promo-123"},
                }
            }
        },
    },
    status.HTTP_400_BAD_REQUEST: common_responses[status.HTTP_400_BAD_REQUEST],
    status.HTTP_404_NOT_FOUND: common_responses[status.HTTP_404_NOT_FOUND],
    status.HTTP_500_INTERNAL_SERVER_ERROR: common_responses[
        status.HTTP_500_INTERNAL_SERVER_ERROR
    ],
}

activate_promotion_examples = {
    status.HTTP_200_OK: {
        "description": "Promotion activated successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "Promotion activated successfully.",
                }
            }
        },
    },
    status.HTTP_400_BAD_REQUEST: common_responses[status.HTTP_400_BAD_REQUEST],
    status.HTTP_404_NOT_FOUND: common_responses[status.HTTP_404_NOT_FOUND],
    status.HTTP_500_INTERNAL_SERVER_ERROR: common_responses[
        status.HTTP_500_INTERNAL_SERVER_ERROR
    ],
}


deactivate_promotion_examples = {
    status.HTTP_200_OK: {
        "description": "Promotion deactivated successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "Promotion deactivated successfully.",
                }
            }
        },
    },
    status.HTTP_400_BAD_REQUEST: common_responses[status.HTTP_400_BAD_REQUEST],
    status.HTTP_404_NOT_FOUND: common_responses[status.HTTP_404_NOT_FOUND],
    status.HTTP_500_INTERNAL_SERVER_ERROR: common_responses[
        status.HTTP_500_INTERNAL_SERVER_ERROR
    ],
}


extend_promotion_examples = {
    status.HTTP_200_OK: {
        "description": "Promotion extended successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "Promotion extended successfully.",
                }
            }
        },
    },
    status.HTTP_400_BAD_REQUEST: common_responses[status.HTTP_400_BAD_REQUEST],
    status.HTTP_404_NOT_FOUND: common_responses[status.HTTP_404_NOT_FOUND],
    status.HTTP_500_INTERNAL_SERVER_ERROR: common_responses[
        status.HTTP_500_INTERNAL_SERVER_ERROR
    ],
}


get_promotion_by_id_examples = {
    status.HTTP_200_OK: {
        "description": "Promotion retrieved successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "Promotions retrieved successfully.",
                    "data": {
                        "id": "promo-123",
                        "name": "Promotion 1",
                        "start_date": "2023-10-01T00:00:00Z",
                        "end_date": "2023-10-31T23:59:59Z",
                        "is_active": True,
                        "description": "10% off on all products",
                        "max_uses": 100,
                        "current_uses": 50,
                        "discount_value": 10,
                        "promotion_type": "percentage",
                        "rule": {
                            "min_quantity": 1,
                            "max_quantity": 10,
                            "applicable_products": ["prod-1", "prod-2"],
                        },
                        "created_at": "2023-09-01T12:00:00Z",
                        "updated_at": "2023-09-15T12:00:00Z",
                        "products": [
                            {"id": "prod-1", "name": "Product 1"},
                            {"id": "prod-2", "name": "Product 2"},
                        ],
                    },
                    "error": None,
                    "paginationMetadata": {},
                }
            }
        },
    },
    status.HTTP_400_BAD_REQUEST: common_responses[status.HTTP_400_BAD_REQUEST],
    status.HTTP_404_NOT_FOUND: common_responses[status.HTTP_404_NOT_FOUND],
    status.HTTP_500_INTERNAL_SERVER_ERROR: common_responses[
        status.HTTP_500_INTERNAL_SERVER_ERROR
    ],
}


list_promotions_examples = {
    status.HTTP_200_OK: {
        "description": "Promotions retrieved successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "message": "Promotions retrieved successfully.",
                    "data": [
                        {
                            "id": "promo-123",
                            "name": "Promotion 1",
                            "start_date": "2023-10-01T00:00:00Z",
                            "end_date": "2023-10-31T23:59:59Z",
                            "is_active": True,
                            "description": "10% off on all products",
                            "max_uses": 100,
                            "current_uses": 50,
                            "discount_value": 10,
                            "promotion_type": "percentage",
                            "rule": {
                                "min_quantity": 1,
                                "max_quantity": 10,
                                "applicable_products": ["prod-1", "prod-2"],
                            },
                            "created_at": "2023-09-01T12:00:00Z",
                            "updated_at": "2023-09-15T12:00:00Z",
                            "products": [
                                {"id": "prod-1", "name": "Product 1"},
                                {"id": "prod-2", "name": "Product 2"},
                            ],
                        },
                        {
                            "id": "promo-456",
                            "name": "Promotion 2",
                            "start_date": "2023-10-15T00:00:00Z",
                            "end_date": "2023-11-15T23:59:59Z",
                            "is_active": True,
                            "description": "20% off on selected products",
                            "max_uses": 50,
                            "current_uses": 20,
                            "discount_value": 20,
                            "promotion_type": "percentage",
                            "rule": {
                                "min_quantity": 1,
                                "max_quantity": 5,
                                "applicable_products": ["prod-2", "prod-4"],
                            },
                        },
                    ],
                    "error": None,
                    "paginationMetadata": {
                        "currentPage": 1,
                        "totalPages": 1,
                        "totalItems": 2,
                        "itemsPerPage": 10,
                        "hasNextPage": False,
                        "hasPreviousPage": False,
                    },
                }
            }
        },
    },
    status.HTTP_400_BAD_REQUEST: common_responses[status.HTTP_400_BAD_REQUEST],
    status.HTTP_404_NOT_FOUND: common_responses[status.HTTP_404_NOT_FOUND],
    status.HTTP_500_INTERNAL_SERVER_ERROR: common_responses[
        status.HTTP_500_INTERNAL_SERVER_ERROR
    ],
}
