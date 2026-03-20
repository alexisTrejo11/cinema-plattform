from app.shared.docs.common_responses import (
    common_error_responses,
    common_public_error_responses,
)
from fastapi import status


create_product_examples = {
    **common_error_responses,
    status.HTTP_201_CREATED: {
        "description": "Product created successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "data": {
                        "id": "75bb2bef-953f-47b2-8e48-6f3101515ebe",
                        "name": "Pizza Margherita",
                        "price": 12.99,
                        "category_id": 1,
                        "description": "Classic pizza with tomato sauce and mozzarella",
                        "image_url": "http://example.com/pizza.jpg",
                        "preparation_time": 20,
                        "calories": 250,
                    },
                    "error": None,
                    "timestamp": "2023-10-01T12:00:00Z",
                }
            }
        },
    },
}

create_update_examples = {
    **common_error_responses,
    status.HTTP_200_OK: {
        "description": "Product updated successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "data": {
                        "id": "75bb2bef-953f-47b2-8e48-6f3101515ebe",
                        "name": "Pizza Margherita Updated",
                        "price": 16.99,
                        "category_id": 2,
                        "description": "Classic pizza with tomato sauce and mozzarella",
                        "image_url": "http://example.com/pizza_updated.jpg",
                        "preparation_time": 22,
                        "calories": 240,
                    },
                }
            }
        },
    },
}

delete_product_examples = {
    **common_error_responses,
    status.HTTP_200_OK: {
        "description": "Product deleted successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "data": None,
                    "message": "Product deleted successfully.",
                    "error": None,
                    "timestamp": "2023-10-01T12:00:00Z",
                }
            }
        },
    },
}

get_product_examples = {
    **common_public_error_responses,
    status.HTTP_200_OK: {
        "description": "Product retrieved successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "data": {
                        "id": "75bb2bef-953f-47b2-8e48-6f3101515ebe",
                        "name": "Pizza Margherita",
                        "price": 12.99,
                        "category_id": 1,
                        "description": "Classic pizza with tomato sauce and mozzarella",
                        "image_url": "http://example.com/pizza.jpg",
                        "preparation_time": 20,
                        "calories": 250,
                    },
                    "error": None,
                    "timestamp": "2023-10-01T12:00:00Z",
                }
            }
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Not Found: The requested resource was not found.",
        "content": {
            "application/json": {
                "examples": {
                    "user_not_found": {
                        "summary": "Resource not found",
                        "value": {
                            "message": "Resource not found.",
                            "data": None,
                            "error": "RESOURCE_NOT_FOUND",
                        },
                    }
                }
            }
        },
    },
}

search_products_examples = {
    **common_public_error_responses,
    status.HTTP_200_OK: {
        "description": "Products retrieved successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "data": [
                        {
                            "id": "75bb2bef-953f-47b2-8e48-6f3101515ebe",
                            "name": "Pizza Margherita",
                            "price": 12.99,
                            "category_id": 1,
                            "description": "Classic pizza with tomato sauce and mozzarella",
                            "image_url": "http://example.com/pizza.jpg",
                            "preparation_time": 20,
                            "calories": 250,
                        },
                        {
                            "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
                            "name": "Spaghetti Carbonara",
                            "price": 10.99,
                            "category_id": 2,
                            "description": "Creamy pasta with pancetta and cheese",
                            "image_url": "http://example.com/spaghetti.jpg",
                            "preparation_time": 15,
                            "calories": 400,
                        },
                    ],
                    "error": None,
                    "timestamp": "2023-10-01T12:00:00Z",
                    "metadata": {
                        "page": {
                            "offset": 0,
                            "limit": 10,
                            "total_items": 2,
                            "total_pages": 1,
                        }
                    },
                }
            }
        },
    },
}


get_category_examples = {
    **common_public_error_responses,
    status.HTTP_200_OK: {
        "description": "Category retrieved successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "data": {
                        "id": 1,
                        "name": "Pizzas",
                        "description": "Various pizza types",
                        "is_active": True,
                    },
                    "error": None,
                    "timestamp": "2023-10-01T12:00:00Z",
                }
            }
        },
    },
    status.HTTP_404_NOT_FOUND: {
        "description": "Not Found: The requested product category was not found.",
        "content": {
            "application/json": {
                "examples": {
                    "category_not_found": {
                        "summary": "Resource not found",
                        "value": {
                            "message": "Category not found.",
                            "data": None,
                            "error": "CATEGORY_NOT_FOUND",
                        },
                    }
                }
            }
        },
    },
}

create_category_examples = {
    **common_error_responses,
    status.HTTP_201_CREATED: {
        "description": "Category created successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "data": {
                        "id": 1,
                        "name": "Pizzas",
                        "description": "Various pizza types",
                        "is_active": True,
                    },
                    "error": None,
                    "timestamp": "2023-10-01T12:00:00Z",
                }
            }
        },
    },
}

list_categories_examples = {
    **common_public_error_responses,
    status.HTTP_200_OK: {
        "description": "List of product categories",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "data": [
                        {
                            "id": 1,
                            "name": "Pizzas",
                            "description": "Various pizza types",
                            "is_active": True,
                        },
                        {
                            "id": 2,
                            "name": "Pastas",
                            "description": "Different pasta dishes",
                            "is_active": True,
                        },
                    ],
                    "error": None,
                    "timestamp": "2023-10-01T12:00:00Z",
                }
            }
        },
    },
}

delete_category_examples = {
    **common_error_responses,
    status.HTTP_200_OK: {
        "description": "Category deleted successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "data": None,
                    "error": None,
                    "timestamp": "2023-10-01T12:00:00Z",
                }
            }
        },
    },
}

update_category_examples = {
    **common_error_responses,
    status.HTTP_200_OK: {
        "description": "Category updated successfully",
        "content": {
            "application/json": {
                "example": {
                    "success": True,
                    "data": {
                        "id": 1,
                        "name": "Updated Pizzas",
                        "description": "Updated description for pizza types",
                        "is_active": True,
                    },
                    "error": None,
                    "timestamp": "2023-10-01T12:00:00Z",
                }
            }
        },
    },
}
